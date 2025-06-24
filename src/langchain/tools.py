from langchain.tools import tool
from src.database.database import Database

@tool
async def update_user_name_tool(thread_id: int, name: str) -> str:
    """Actualiza el nombre del usuario asociado a la conversación."""
    db = Database()
    await db.save_user_name(thread_id, name)
    return f"Nombre actualizado a {name}."

@tool
async def get_user_name_tool(thread_id: int) -> str:
    """Devuelve el nombre del usuario asociado a la conversación. Si no está cargado, informa amablemente."""
    db = Database()
    user = await db.get_user_by_thread_id(thread_id)
    if user and user["full_name"]:
        return user["full_name"]
    return "Aún no tengo tu número agregado. ¿Podrías decirme tu nombre para agendarlo?"