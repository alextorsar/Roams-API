from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from routes.auth import router as auth_router
from routes.conversation import router as conversation_router
from routes.message import router as message_router
from core.logging import logger

app = FastAPI(
    title="Rest API",
    description="API for backend of a conversational chatbot",
    version="1.0.0",
    contact={
        "name": "Alex",
        "email": "alejandro.torres.sar@gmail.com",
    },
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Leer el cuerpo de la solicitud
        body = await request.body()
        logger.info(f"Incoming request: {request.method} {request.url} - Body: {body.decode('utf-8')}")

        # Procesar la respuesta
        response = await call_next(request)

        # Leer el cuerpo de la respuesta
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        logger.info(f"Response: {response.status_code} - Body: {response_body.decode('utf-8') if response_body else 'No body'}")

        # Crear una nueva respuesta con el mismo cuerpo
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

# Agregar el middleware personalizado
app.add_middleware(LoggingMiddleware)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(conversation_router, prefix="/conversation", tags=["Conversation"])
app.include_router(message_router, prefix="/message", tags=["Message"])