from typing import Dict
from src.settings import settings
from src.agent.agent import ChatAgent
from src.integrations.whatsapp_integration import WhatsAppService
from src.utils.helpers import parse_whatsapp_payload, mask_phone
from src.database.database import Database

class WhatsAppController:
    def __init__(self):
        """
        Inicializa la integración de WhatsApp.
        """
        self.chat_agent = ChatAgent()
        self.whatsapp_service = WhatsAppService()
        self.chat_history = []
        self.database = Database()

    async def validate_webhook(self, params: Dict[str, str]) -> bool:
        """
        Valida el webhook de WhatsApp.

        Args:
            params: Parámetros de la solicitud

        Returns:
            True si la validación es exitosa, False en caso contrario
        """
        mode = params.get("hub.mode")
        challenge = params.get("hub.challenge")
        token = params.get("hub.verify_token")

        return (
            mode == "subscribe" and
            token == settings.VERIFY_TOKEN and
            challenge is not None
        )
    
    async def handle_incoming_message(self, data: Dict) -> None:
        """
        Maneja los mensajes entrantes de WhatsApp.

        Args:
            data: Datos del mensaje entrante

        Returns:
            None
        """
        # Aquí puedes implementar la lógica para manejar el mensaje entrante
        # Por ejemplo, guardar en una base de datos, enviar una respuesta, etc.
        parsed_data = parse_whatsapp_payload(data)
        sanitized = parsed_data.copy()
        if sanitized.get("phone"):
            sanitized["phone"] = mask_phone(sanitized["phone"])
        print(f"Parsed data: {sanitized}")

        if parsed_data["success"] == False:
            return None
        
        message_id = parsed_data.get("message_id")
        if message_id:
            already_processed = await self.database.is_message_processed(message_id)
            if already_processed:
                print(f"Mensaje duplicado ignorado: {message_id}")
                return None
        
        # Verificar si el usuario ya existe en la base de datos
        user_data = await self.database.get_user_by_phone(parsed_data['phone'])

        if not user_data:
            # Si el usuario no existe, registrarlo
            user_data = await self.database.register_user(
                fullname=parsed_data['full_name'],
                phone=parsed_data['phone']
            )

        conversation, self.chat_history = await self.database.get_or_create_recent_conversation(user_data.id)
        response_state = await self.chat_agent.run(
            input_text=parsed_data['text'],
            chat_history=self.chat_history,
            thread_id=conversation['id'],
            conversation_faqs_id=conversation['faq_ids']
        )

        await self.whatsapp_service.send_message(parsed_data['phone'], response_state.response)

        mensajes_a_guardar = []
        if response_state.messages:
            # Último mensaje del usuario (si hay al menos dos)
            if len(response_state.messages) >= 2:
                mensajes_a_guardar.append(response_state.messages[-2])
            # Última respuesta del bot
            mensajes_a_guardar.append(response_state.messages[-1])

        await self.database.save_chat_history(parsed_data.get("message_id"), conversation['id'], mensajes_a_guardar)

        return None



