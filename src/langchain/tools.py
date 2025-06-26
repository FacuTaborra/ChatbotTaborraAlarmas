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
async def homeassistant_webhook(thread_id: int, action: str, info: str = None) -> str:
    """
    Llama a un webhook de HomeAssistant si el usuario pide acciones relacionadas con la alarma.
    El parámetro 'action' define la acción a realizar (ej: 'escaneo', 'estadoAlarma').
    Si la acción requiere una cámara, pasa el nombre en 'info'.
    """
    try: 
        payload = {"action": action}
        if info:
            payload["camara"] = info
        ha = HomeAssistantIntegration()
        response = await ha.homeassistant_webhook(thread_id, payload)
        return response
    except Exception as e:
        return 'No se pudo ejecutar la acción'

@tool
async def faq_tool(thread_id: int, question: str) -> str:
    """
    Esta herramienta es para consultar sobre preguntas frecuentes o problemas que puede tener un cliente segun el tipo de la alarma.
    Utiliza la informacion para explicar un paso a paso lo mas simple posible, no envies el texto tal cual solo la informacion necesaria.
    """
    db = Database()
    user = await db.get_user_by_thread_id(thread_id, "level")
    if not user or user.get("level", 0) < 2:
        return "No tienes permisos para ver esta información."
    faq = await db.search_faq(question)
    if not faq:
        return "No encontré una respuesta en las FAQs."
    text = faq.get("desc_faq", "")
    if faq.get("link"):
        text += f"\nVideo: {faq['link']}"
    return text

@tool
async def log_user_faq_tool(thread_id: int, faq_id: int, is_done: bool = False) -> str:
    """Guarda en la base qué FAQ vio el usuario y si se resolvió."""
    db = Database()
    ok = await db.log_user_faq(thread_id, faq_id, is_done)
    if ok:
        return "FAQ registrada"
    return "No se pudo registrar la FAQ"