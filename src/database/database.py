import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import asyncmy
from src.settings import settings
from src.database.models import User, Conversation, Message
from datetime import datetime, timedelta
from langchain_core.messages import HumanMessage, AIMessage

class Database:
    def __init__(self):
        self.read_pool = None
        self.write_pool = None

    async def connect(self) -> Tuple[asyncmy.Pool, asyncmy.Pool]:
            """Establece los pools de conexión para lectura y escritura.

            Returns:
                Tupla con los pools de lectura y escritura
            """
            if not self.read_pool:
                self.read_pool = await asyncmy.create_pool(
                    host=settings.DB_HOST,
                    port=int(settings.DB_PORT),
                    user=settings.DB_USER_READER,
                    password=settings.DB_PASS_READER,
                    database=settings.DB_NAME,
                    autocommit=True,  # Para operaciones de solo lectura
                    charset="utf8mb4",  # Añadir esta línea
                    use_unicode=True   # Añadir esta línea
                )
            if not self.write_pool:
                # Para operaciones de escritura, desactivamos autocommit para manejar la transacción manualmente.
                self.write_pool = await asyncmy.create_pool(
                    host=settings.DB_HOST,
                    port=int(settings.DB_PORT),
                    user=settings.DB_USER_WRITER,
                    password=settings.DB_PASS_WRITER,
                    database=settings.DB_NAME,
                    autocommit=False,
                    charset="utf8mb4",  # Añadir esta línea
                    use_unicode=True    # Añadir esta línea
                )
            return self.read_pool, self.write_pool

    async def close(self) -> None:
        """Cierra ambos pools de conexión."""
        if self.read_pool:
            self.read_pool.close()
            await self.read_pool.wait_closed()
            self.read_pool = None
        if self.write_pool:
            self.write_pool.close()
            await self.write_pool.wait_closed()
            self.write_pool = None

    async def get_user_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Recupera un usuario usando el pool de lectura.
        Args:
            phone: Número de teléfono del usuario

        Returns:
            Datos del usuario o None si no existe
        """
        query = "SELECT id, full_name, phone, level FROM users WHERE phone = %s"
        # Asegurarse de que el pool se ha inicializado
        await self.connect()
        async with self.read_pool.acquire() as conn:
            async with conn.cursor(asyncmy.cursors.DictCursor) as cursor:
                await cursor.execute(query, (phone,))
                result = await cursor.fetchone()
                if result:
                    return User(**result)
                return result

    async def register_user(self, fullname: str, phone: str) -> bool:
        """Registra un nuevo usuario con nivel 1 utilizando una transacción.

        Args:
            fullname: Nombre completo del usuario
            phone: Número de teléfono

        Returns:
            True si se registró correctamente
        """
        await self.connect()
        query = """
        INSERT INTO users (full_name, phone, level)
        VALUES (%s, %s, 1)
        """
        async with self.write_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (fullname, phone))
                await cursor.execute("SELECT LAST_INSERT_ID()")
                user_id = (await cursor.fetchone())[0]
                await conn.commit()
                user = User(id=user_id, full_name=fullname, phone=phone, level=1)
                return user


    async def get_or_create_recent_conversation(self, user_id: int):
        """
        Busca una conversación activa en los últimos 30 minutos para el usuario.
        Si no existe, crea una nueva.
        Devuelve (conversation, chat_history)
        """
        await self.connect()
        now = datetime.utcnow()
        thirty_minutes_ago = now - timedelta(minutes=30)
        # Traer conversación y mensajes en una sola consulta JOIN
        query = """
        SELECT c.id as conversation_id, c.user_id, c.started_at, c.is_active,
               m.sender, m.content, m.timestamp
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        WHERE c.user_id = %s AND c.is_active = 1 AND c.started_at >= %s
        ORDER BY c.started_at DESC, m.timestamp ASC
        """
        async with self.read_pool.acquire() as conn:
            async with conn.cursor(asyncmy.cursors.DictCursor) as cursor:
                await cursor.execute(query, (user_id, thirty_minutes_ago))
                rows = await cursor.fetchall()

        if rows:
            # Hay al menos una conversación, armar datos y chat_history
            first = rows[0]
            conversation = {
                "id": first["conversation_id"],
                "user_id": first["user_id"],
                "started_at": first["started_at"],
                "is_active": first["is_active"]
            }
            chat_history = []
            for row in rows:
                if row["sender"] and row["content"] is not None:
                    if row["sender"] == "user":
                        chat_history.append(HumanMessage(content=row["content"]))
                    else:
                        chat_history.append(AIMessage(content=row["content"]))
            return conversation, chat_history
        else:
            # Crear nueva conversación
            insert_query = """
            INSERT INTO conversations (user_id, started_at, is_active)
            VALUES (%s, %s, 1)
            """
            now = datetime.utcnow()
            async with self.write_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(insert_query, (user_id, now))
                    await conn.commit()
                    await cursor.execute("SELECT LAST_INSERT_ID()")
                    conversation_id = (await cursor.fetchone())[0]
            conversation = {
                "id": conversation_id,
                "user_id": user_id,
                "started_at": now,
                "is_active": 1
            }
            return conversation, []
        
    async def save_chat_history(self, conversation_id: int, chat_history: list):
        """
        Guarda todos los mensajes de chat_history en la conversación indicada.
        Cada mensaje debe ser instancia de HumanMessage o AIMessage.
        """
        await self.connect()
        insert_query = """
        INSERT INTO messages (conversation_id, sender, content, timestamp, type)
        VALUES (%s, %s, %s, %s, %s)
        """
        async with self.write_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for msg in chat_history:
                    if hasattr(msg, "content"):
                        sender = "user" if msg.__class__.__name__ == "HumanMessage" else "bot"
                        content = msg.content
                        msg_type = "text"
                        timestamp = getattr(msg, "timestamp", datetime.utcnow())
                        await cursor.execute(insert_query, (
                            conversation_id, sender, content, timestamp, msg_type
                        ))
                await conn.commit()