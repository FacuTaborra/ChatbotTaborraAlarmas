from typing import Dict, Any, List, Optional
import aiohttp
from src.settings import settings


class WhatsAppService:
    def __init__(self, phone_id: Optional[str] = None, access_token: Optional[str] = None):
        """
        Inicializa el servicio de WhatsApp.

        Args:
            phone_id: ID del teléfono en WhatsApp Business API
            access_token: Token de acceso
        """
        self.phone_id = phone_id or settings.WHATSAPP_PHONE_ID
        self.access_token = access_token or settings.WHATSAPP_ACCESS_TOKEN

        if not self.phone_id or not self.access_token:
            print("⚠️ El servicio de WhatsApp está deshabilitado")
            self.enabled = False
        else:
            self.enabled = True
            self.api_url = f"https://graph.facebook.com/v23.0/{self.phone_id}/messages"
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

    async def send_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Envía un mensaje de texto.

        Args:
            to: Número de teléfono destino
            message: Texto del mensaje

        Returns:
            Respuesta de la API
        """
        if not self.enabled:
            return {"error": "El servicio de WhatsApp está deshabilitado"}

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }

        return await self._send_request(payload, f"mensaje a {to}")

    async def send_image(self, to: str, image_url: str, caption: str = "") -> Dict[str, Any]:
        """
        Envía una imagen.

        Args:
            to: Número de teléfono destino
            image_url: URL de la imagen
            caption: Pie de foto opcional

        Returns:
            Respuesta de la API
        """
        if not self.enabled:
            return {"error": "El servicio de WhatsApp está deshabilitado"}

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url, "caption": caption}
        }

        return await self._send_request(payload, f"imagen a {to}")

    async def _send_request(self, payload: Dict[str, Any], action_desc: str) -> Dict[str, Any]:
        """
        Envía una solicitud a la API de WhatsApp.

        Args:
            payload: Datos a enviar
            action_desc: Descripción para logs

        Returns:
            Respuesta de la API
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=10
            ) as response:
                response_data = await response.json()

                if response.status == 200:
                    print(
                        f"✅ Éxito enviando {action_desc}: {response_data}")
                else:
                    print(
                        f"⚠️ Error enviando {action_desc}: {response_data}")
                return response_data
