from fastapi import APIRouter, Request, HTTPException
from src.integrations.whatsapp_integration import WhatsAppIntegration

router = APIRouter()
whatsapp = WhatsAppIntegration()

@router.get("/whatsapp")
async def validate_webhook(request: Request):
    try:
        # Validar webhook
        is_valid = await whatsapp.validate_webhook(dict(request.query_params))

        if is_valid:
            # Meta espera recibir el challenge como número entero
            return int(request.query_params.get("hub.challenge", 0))

        raise HTTPException(status_code=403, detail="Verificación fallida")

    except Exception as e:
        print(f"❌ Error en validación de webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e