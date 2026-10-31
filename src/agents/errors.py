"""Errores de los agentes: traduce las fallas de OpenAI a mensajes claros."""

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ContentFilterFinishReasonError,
    LengthFinishReasonError,
    OpenAIError,
    RateLimitError,
)


class AgentError(Exception):
    """Un agente no pudo completar su tarea."""


def describe_openai_error(agent_name: str, error: OpenAIError) -> str:
    """Devuelve un mensaje accionable según el tipo de falla de OpenAI."""
    if isinstance(error, APITimeoutError):
        return f"{agent_name}: timeout de OpenAI. Probá de nuevo o subí OPENAI_TIMEOUT_SECONDS."
    if isinstance(error, APIConnectionError):
        return f"{agent_name}: no se pudo conectar con OpenAI. Revisá tu conexión."
    if isinstance(error, RateLimitError):
        return f"{agent_name}: límite de uso de OpenAI alcanzado (rate limit o sin crédito)."
    if isinstance(error, AuthenticationError):
        return f"{agent_name}: OpenAI rechazó la clave. Revisá OPENAI_API_KEY en tu .env."
    if isinstance(error, LengthFinishReasonError):
        return f"{agent_name}: la respuesta se cortó por límite de tokens."
    if isinstance(error, ContentFilterFinishReasonError):
        return f"{agent_name}: OpenAI bloqueó la respuesta por su filtro de contenido."
    if isinstance(error, BadRequestError) and error.code == "context_length_exceeded":
        return f"{agent_name}: los documentos superan el límite de tokens del modelo."
    return f"{agent_name}: error de OpenAI ({error})."
