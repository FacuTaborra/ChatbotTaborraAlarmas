from typing import Optional
import aiohttp
from src.database.database import Database

class HomeAssistantIntegration:
    def __init__(self, webhook_url: Optional[str] = None, token: Optional[str] = None):
        """
        Inicializa la herramienta para comunicarse con Home Assistant vía webhook.

        Args:
            webhook_url: URL del webhook configurado en Home Assistant del cliente
            token: Token de autenticación para el webhook
        """
        self.webhook_url = webhook_url
        self.token = token

        if not self.webhook_url:
            print("⚠️ No se ha configurado un webhook para Home Assistant")
            self.enabled = False
        else:
            self.enabled = True

    async def homeassistant_webhook(self, thread_id: int, webhook_url: str = None, payload: dict = None) -> str:
        db = Database()
        user = await db.get_user_by_thread_id(thread_id, 'level')
        if not user:
            return "Usuario no encontrado."
        if user.get("level", 0) < 3:
            return "No tienes permisos para ejecutar esta acción."
        if user.get("level") == 3:
            return "La alarma esta activada"
