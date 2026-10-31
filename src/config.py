"""Configuración: lee variables del .env."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    vision_model: str
    agent_model: str
    request_timeout: float
    max_retries: int
    vision_max_tokens: int


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("Falta OPENAI_API_KEY. Copiá .env.example a .env y completá tu clave.")
    return Settings(
        openai_api_key=api_key,
        vision_model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o"),
        agent_model=os.getenv("OPENAI_AGENT_MODEL", "gpt-4o"),
        request_timeout=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60")),
        max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")),
        vision_max_tokens=int(os.getenv("VISION_MAX_TOKENS", "4096")),
    )
