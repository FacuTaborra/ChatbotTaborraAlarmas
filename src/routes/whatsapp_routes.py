from fastapi import APIRouter, Request, HTTPException
from src.controllers.whatsapp_controller import WhatsAppController

router = APIRouter()
whatsapp = WhatsAppController()

@router.get("/whatsapp")
async def validate_webhook(request: Request):
    is_valid = await whatsapp.validate_webhook(dict(request.query_params))
    if is_valid:
        return int(request.query_params.get("hub.challenge", 0))
    raise HTTPException(status_code=403, detail="Verificación fallida")

    
@router.post("/whatsapp")
async def handle_webhook(request: Request):
    data = await request.json()
    response = await whatsapp.handle_incoming_message(data)
    return {"status": "ok"}