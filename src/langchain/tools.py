from langchain.tools import tool
from src.database.database import Database
from src.integrations.homeassistant_integration import HomeAssistantIntegration


@tool
async def update_user_name_tool(thread_id: int, name: str) -> str:
    """Actualiza el nombre del usuario asociado a la conversación."""
    db = Database()
    await db.save_user_name(thread_id, name)
    return f"Nombre actualizado a {name}."

@tool
async def get_user_name_tool(thread_id: int) -> str:
    """
    Herramienta para obtener el nombre, solo utiliza el nombre en la conversación si es necesario, pero nunca saludes ni repitas saludos automáticos.
    """
    db = Database()
    user = await db.get_user_by_thread_id(thread_id, 'full_name')
    if user and user["full_name"]:
        return user["full_name"]
    return "Aún no tengo tu número agregado. ¿Podrías decirme tu nombre para agendarlo?"

@tool
async def homeassistant_webhook(thread_id: int, webhook_url: str = None, payload: dict = None) -> str:
    """
    Llama a un webhook de HomeAssistant si el usuario pide acciones relacionadas con la alarma.
    Pueden ser acciones como pedir el estado de la alarma o ver imagenes de la camara.
    Informa amablemente segun si tiene acceso o no a esa funcion.
    en payload debes pones lo que quiere el usuario.
    """
    ha = HomeAssistantIntegration()
    response = await ha.homeassistant_webhook(thread_id, webhook_url, payload)
    return response


