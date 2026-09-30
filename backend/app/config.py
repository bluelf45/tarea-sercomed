from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SYSTEM_PROMPT = (
    "Eres un asistente virtual amable y profesional. Responde siempre en español, "
    "de forma clara y concisa. Usa únicamente la información incluida en la sección "
    "<conocimiento>. Si la respuesta no está ahí, dilo con honestidad y sugiere al "
    "usuario contactar directamente a la organización. No inventes datos."
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    model: str = "claude-haiku-4-5"
    max_tokens: int = 1024
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    knowledge_dir: Path = Path(__file__).resolve().parent.parent / "knowledge"
    max_history: int = 40
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
