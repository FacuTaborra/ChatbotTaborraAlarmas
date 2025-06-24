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
        await self.connect()
        now = datetime.utcnow()
        thirty_minutes_ago = now - timedelta(minutes=30)
        # Traer solo la conversación más reciente
        query_conv = """
        SELECT id, user_id, started_at
        FROM conversations
        WHERE user_id = %s AND started_at >= %s
        ORDER BY started_at DESC
        LIMIT 1
        """
        async with self.read_pool.acquire() as conn:
            async with conn.cursor(asyncmy.cursors.DictCursor) as cursor:
                await cursor.execute(query_conv, (user_id, thirty_minutes_ago))
                conv = await cursor.fetchone()

        if conv:
            conversation = {
                "id": conv["id"],
                "user_id": conv["user_id"],
                "started_at": conv["started_at"],
            }
            # Traer solo los mensajes de esa conversación
            query_msgs = """
            SELECT message_id, sender, content, timestamp, type
            FROM messages
            WHERE conversation_id = %s
            ORDER BY timestamp ASC
            """
            async with self.read_pool.acquire() as conn:
                async with conn.cursor(asyncmy.cursors.DictCursor) as cursor:
                    await cursor.execute(query_msgs, (conv["id"],))
                    rows = await cursor.fetchall()
            chat_history = []
            for row in rows:
                if row["message_id"] and row["content"] is not None:
                    if row["sender"] == "user":
                        chat_history.append(HumanMessage(
                            content=row["content"],
                            additional_kwargs={},
                            response_metadata={},
                        ))
                    elif row["sender"] == "bot":
                        chat_history.append(AIMessage(
                            content=row["content"],
                            additional_kwargs={},
                            response_metadata={},
                        ))
            return conversation, chat_history
        else:
            # Crear nueva conversación
            insert_query = """
            INSERT INTO conversations (user_id, started_at)
            VALUES (%s, %s)
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
            }
            return conversation, []
        
    async def save_chat_history(self, message_id: str, conversation_id: int, messages: list):
        """
        Guarda solo los mensajes nuevos en la conversación indicada.
        Cada mensaje debe ser instancia de HumanMessage o AIMessage.
        """
        if not messages:
            return
        await self.connect()
        insert_query = """
        INSERT INTO messages (message_id, conversation_id, sender, content, timestamp, type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        check_query = "SELECT 1 FROM messages WHERE message_id = %s LIMIT 1"
        async with self.write_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for msg in messages:
                    if hasattr(msg, "content"):
                        # Si el mensaje es del usuario, usa el message_id recibido
                        if msg.__class__.__name__ == "HumanMessage":
                            msg_id = message_id
                        else:
                            # Si es del bot, genera un id único (o usa None para que no choque)
                            msg_id = f"{message_id}_bot"
                        # Verifica si ya existe
                        await cursor.execute(check_query, (msg_id,))
                        exists = await cursor.fetchone()
                        if exists:
                            continue  # Ya existe, no lo insertes
                        sender = "user" if msg.__class__.__name__ == "HumanMessage" else "bot"
                        content = msg.content
                        msg_type = "text"
                        timestamp = getattr(msg, "timestamp", datetime.utcnow())
                        await cursor.execute(insert_query, (
                            msg_id, conversation_id, sender, content, timestamp, msg_type
                        ))
                await conn.commit()
                
    async def save_user_name(self, thread_id: int, name: str) -> bool:
        """
        Actualiza el nombre del usuario asociado a una conversación (thread_id).
        """
        await self.connect()
        # Buscar el user_id asociado a la conversación
        query_user = "SELECT user_id FROM conversations WHERE id = %s"
        async with self.write_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_user, (thread_id))
                result = await cursor.fetchone()
                if not result:
                    return False  # No se encontró la conversación
                user_id = result[0]
                # Actualizar el nombre del usuario
                update_query = "UPDATE users SET full_name = %s WHERE id = %s"
                await cursor.execute(update_query, (name, user_id))
                await conn.commit()
        return True

    async def get_user_by_thread_id(self, thread_id: int) -> Optional[dict]:
        """
        Devuelve los datos del usuario asociado a una conversación (thread_id).
        """
        await self.connect()
        query = """
        SELECT u.full_name
        FROM users u
        JOIN conversations c ON u.id = c.user_id
        WHERE c.id = %s
        """
        async with self.read_pool.acquire() as conn:
            async with conn.cursor(asyncmy.cursors.DictCursor) as cursor:
                await cursor.execute(query, (thread_id,))
                result = await cursor.fetchone()
                if result:
                    return dict(result)
                return
            

    async def is_message_processed(self, message_id: str) -> bool:
        """
        Verifica si un mensaje ya fue procesado usando su message_id.

        Args:
            message_id: ID único del mensaje de WhatsApp

        Returns:
            True si el mensaje ya existe en la base de datos, False si no.
        """
        await self.connect()
        query = """
            SELECT 1 FROM messages WHERE message_id = %s LIMIT 1
        """
        async with self.read_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (message_id,))
                result = await cursor.fetchone()
                return result is not None