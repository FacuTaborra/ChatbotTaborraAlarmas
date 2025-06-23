# src/utils/helpers.py
import unicodedata
from typing import Dict, Any
import tiktoken
import src.settings as settings
import PyPDF2



def parse_whatsapp_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa el payload de WhatsApp para extraer información relevante.

    Args:
        data: Payload de WhatsApp

    Returns:
        Diccionario con datos extraídos
    """
    
    result = {
        "success": False,
        "message_id": None,
        "text": None,
        "phone": None,
        "full_name": None
    }

    entry = data.get("entry", [])
    if not entry:
        return result

    changes = entry[0].get("changes", [])
    if not changes:
        return result

    value = changes[0].get("value", {})
    if "statuses" in value:
        return result

    messages = value.get("messages", [])
    if not messages:
        return result

    message_data = messages[0]
    result["message_id"] = message_data.get("id", "")

    # Extraer texto
    if message_data.get("type") == "text":
        result["text"] = message_data.get("text", {}).get("body", "")
    elif message_data.get("type") == "interactive":
        interactive = message_data.get("interactive", {})
        if interactive.get("type") == "button_reply":
            result["text"] = interactive.get(
                "button_reply", {}).get("title", "")

    # Extraer teléfono
    result["phone"] = normalize_phone(message_data.get("from", ""))

    # Extraer nombre completo
    try:
        result["full_name"] = value.get("contacts", [{}])[0]["profile"]["name"]
    except (IndexError, KeyError):
        result["full_name"] = "Usuario"

    if result["message_id"] and result["text"] and result["phone"]:
        result["success"] = True

    return result



def normalize_phone(phone: str) -> str:
    """
    Normaliza un número de teléfono para asegurar un formato consistente.

    Args:
        phone: Número de teléfono

    Returns:
        Número normalizado
    """
    # Quitar espacios y caracteres no numéricos
    phone = ''.join(filter(str.isdigit, phone))

    # Asegurar que tiene formato internacional
    if phone.startswith("549"):
        phone = "54" + phone[3:]
    elif not phone.startswith("54"):
        phone = "54" + phone

    return phone


def trim_chat_history(chat_history, max_tokens=14000, model_name = settings.settings.MODEL) -> list:
    enc = tiktoken.encoding_for_model(model_name)
    trimmed = []
    total_tokens = 0

    # Recorre el historial desde el final (mensajes más recientes)
    for msg in reversed(chat_history):
        # Calcula tokens del mensaje
        tokens = len(enc.encode(msg.content))
        if total_tokens + tokens > max_tokens:
            break
        trimmed.insert(0, msg)  # Inserta al principio para mantener el orden
        total_tokens += tokens

    return trimmed

def load_pdf_text(pdf_path: str) -> str:
    """Carga el texto de un archivo PDF y lo limpia."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = " ".join(lines)
    return clean_text