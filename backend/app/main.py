import logging

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import llm
from .config import settings
from .knowledge import build_system_prompt
from .schemas import ChatRequest, ChatResponse

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Chatbot IA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Se construye una vez al iniciar; reinicia el backend tras editar knowledge/.
SYSTEM_PROMPT = build_system_prompt(settings.system_prompt, settings.knowledge_dir)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": settings.model}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        reply = await llm.chat(SYSTEM_PROMPT, request.messages)
    except anthropic.RateLimitError:
        raise HTTPException(429, "Hay demasiadas solicitudes, intenta de nuevo en un momento.")
    except (anthropic.AuthenticationError, TypeError):
        # TypeError: el SDK no encontró credenciales (ANTHROPIC_API_KEY ausente).
        logger.exception("ANTHROPIC_API_KEY inválida o ausente")
        raise HTTPException(500, "El servicio de IA no está configurado correctamente.")
    except anthropic.APIStatusError as e:
        logger.error("Error de la API de Anthropic: %s", e)
        raise HTTPException(502, "El servicio de IA respondió con un error.")
    except anthropic.APIConnectionError:
        raise HTTPException(503, "No se pudo conectar con el servicio de IA.")
    return ChatResponse(reply=reply)
