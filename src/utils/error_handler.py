from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTP error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"Integrity error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"error": "Error de integridad: datos duplicados o violación de restricción en la base de datos."},
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(request: Request, exc: OperationalError):
        logger.error(f"Operational error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Error operacional: problema de conexión o consulta con la base de datos."},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Error general de base de datos."},
        )

    # Manejo específico para errores de conexión a OpenAI y HTTPX
    try:
        import openai
        from httpx import ConnectError
    except ImportError:
        openai = None
        ConnectError = None

    if openai:
        @app.exception_handler(openai.APIConnectionError)
        async def openai_connection_error_handler(request: Request, exc: Exception):
            logger.error(f"Error de conexión con OpenAI: {str(exc)}")
            return JSONResponse(
                status_code=502,
                content={"error": "No se pudo conectar con la API de OpenAI. Verifica tu conexión a internet o la configuración de la API."},
            )

    if ConnectError:
        @app.exception_handler(ConnectError)
        async def httpx_connect_error_handler(request: Request, exc: Exception):
            logger.error(f"Error de conexión HTTPX: {str(exc)}")
            return JSONResponse(
                status_code=502,
                content={"error": "No se pudo conectar al servidor externo. Verifica tu conexión a internet o la URL de destino."},
            )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.error(f"Value error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Error de valor: {str(exc)}"},
        )

    @app.exception_handler(KeyError)
    async def key_error_handler(request: Request, exc: KeyError):
        logger.error(f"Key error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Falta una clave esperada en los datos: {str(exc)}"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Error inesperado: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": f"Error interno del servidor: {type(exc).__name__}: {str(exc)}"},
        )