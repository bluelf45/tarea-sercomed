import anthropic

from .config import settings
from .schemas import ChatMessage

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key or None)


async def chat(system_prompt: str, messages: list[ChatMessage]) -> str:
    # Recorta el historial y asegura que empiece con un mensaje del usuario.
    history = messages[-settings.max_history :]
    while history and history[0].role != "user":
        history = history[1:]

    response = await client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[m.model_dump() for m in history],
    )
    return "".join(block.text for block in response.content if block.type == "text")
