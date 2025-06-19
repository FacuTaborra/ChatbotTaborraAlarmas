import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from src.routes import whatsapp_routes
from src.utils.error_handler import register_error_handlers

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

register_error_handlers(app)

app.include_router(whatsapp_routes.router, prefix="/webhook", tags=["WhatsApp"])


@app.get("/")
async def index():
    return {"stats": "Api Taborra Alarmas funcionando correctamente!"}