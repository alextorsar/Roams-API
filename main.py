from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.conversation import router as conversation_router
from routes.message import router as message_router

app = FastAPI(
    title="Rest API",
    description="API for backend of a conversational chatbot",
    version="1.0.0",
    contact={
        "name": "Alex",
        "email": "alejandro.torres.sar@gmail.com",
    },
)

# Incluir las rutas
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(conversation_router, prefix="/conversation", tags=["Conversation"])
app.include_router(message_router, prefix="/message", tags=["Message"])