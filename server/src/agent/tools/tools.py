from langchain.tools import tool
from src.database.database import Database
from src.integrations.homeassistant_integration import HomeAssistantIntegration
from src.utils.faq_index import search_faq

@tool
async def update_user_name_tool(thread_id: int, name: str) -> str:
    """Actualiza el nombre del usuario asociado a la conversación."""
    db = Database()
    await db.save_user_name(thread_id, name)
    return f"Nombre actualizado a {name}."

@tool
async def get_user_name_tool(thread_id: int) -> str:
    """
    ↪️ **Cuándo llamarla**
      • Si vas a saludar, despedir o responder con un trato personalizado y todavía NO sabés el nombre.
      • Si el usuario lo solicitó explícitamente (“¿Sabés mi nombre?” o similar).
      • Si pasaron más de X mensajes sin mencionarlo y querés volver a humanizar la conversación.

    🚫 **Cuándo NO llamarla**
      • Ya usaste el nombre en esta misma interacción o está en memoria.
      • El contexto exige anonimato (p.ej., consultas sensibles) o la respuesta no necesita personalización.
    
    📝 **Qué hace**
      Devuelve el `full_name` del usuario asociado al `thread_id`.
      Si no existe, devuelve una frase amigable pidiendo el nombre para agendarlo.

    ✔️ **Ejemplos de uso correcto**
      1. “¡Hola! ¿Cómo puedo ayudarte hoy?” → *No la llames si ya conocés el nombre.*
      2. “¡Genial, Juan!” → *No la llames, ya tenés el nombre.*
      3. “Quiero saber el estado de mi sistema.” → *Llamala si no hay nombre registrado.*
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
    🔧 **Tool `faq_tool` – Guía paso a paso para resolver problemas o preguntas frecuentes de la alarma**

    **Cuándo usarla**  
    ─────────────────  
    Invócala **solo** cuando el usuario describa un inconveniente concreto con
    su sistema de alarma y **ya hayas confirmado**:
      1. El **modelo de alarma**.  
      2. Cualquier dato extra imprescindible (partición, zona, tipo de aviso).

    Si el cliente todavía no proporcionó esa información, pídesela antes de
    llamar a la herramienta. El LLM debería formular las preguntas necesarias
    (ej.: “¿Qué modelo de alarma tienes?” o “¿La sirena hace un pitido corto o
    continuo?”) para obtener contexto suficiente.

    **Formato de respuesta**
    ─────────────────────── 
    Agregarle emojis a esto para que quede mejor pero la estructura es la misma.

    ```
    Solución encontrada
    Alarma: <modelo>
    Problema: <título FAQ>

    Pasos:
    1. <paso 1>
    2. <paso 2>
    …

    Video: <link> -> debes enviarlo siempre si es que lo tiene.
    ```
    El agente **no** debe alterar este layout.
    """
    try:
        db = Database()
        user = await db.get_user_by_thread_id(thread_id, "level")
        if not user or user.get("level", 0) < 2:
            return "Lo siento, no tienes permisos para ver esta información. Si eres cliente por favor, comunicate con el servicio tecnico o con el equipo de ventas"
        faq = await search_faq(question)
        if not faq:
            return "No encontré una respuesta en las FAQs."
        texto = faq.get("desc_faq", "")
        if faq.get("video_link"):
            texto += f"\nVideo: {faq['video_link']}"
        return texto
    except Exception as e:
        print(e)
        return 'Error al buscar FAQs'


@tool
async def log_user_faq_tool(thread_id: int, faq_id: int, is_done: bool = False) -> str:
    """Guarda en la base qué FAQ vio el usuario y si se resolvió."""
    db = Database()
    ok = await db.log_user_faq(thread_id, faq_id, is_done)
    if ok:
        return "FAQ registrada"
    return "No se pudo registrar la FAQ"
