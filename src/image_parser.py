"""Validación de imágenes, encoding base64 y llamada multimodal a GPT-4o."""

import base64
from pathlib import Path

from openai import APIConnectionError, APITimeoutError, BadRequestError, OpenAI, RateLimitError

from src.config import get_settings

# Extensión -> tipo MIME que espera la API en el data URL
MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

# Primeros bytes ("firma") de cada formato: detectan archivos renombrados o corruptos
MAGIC_BYTES = {"image/png": b"\x89PNG", "image/jpeg": b"\xff\xd8\xff"}

VISION_PROMPT = (
    "You are a legal document transcriber. Transcribe the full text of this contract image "
    "as faithfully as possible, in its original language (Spanish). "
    "Preserve the hierarchy: title, parties, numbered clauses with their titles, sections and lists, "
    "each on its own line. Do not summarize, translate, correct or interpret anything. "
    "If a word is illegible, write [ilegible]. Return only the transcribed text."
)


class ImageParsingError(Exception):
    """Error al validar la imagen o al transcribirla con GPT-4o."""


def validate_image(image_path: str) -> str:
    """Verifica que el archivo exista y sea PNG/JPEG real. Devuelve su tipo MIME."""
    path = Path(image_path)
    if not path.is_file():
        raise ImageParsingError(f"No existe el archivo: {image_path}")

    mime_type = MIME_TYPES.get(path.suffix.lower())
    if mime_type is None:
        raise ImageParsingError(f"Formato no soportado '{path.suffix}' en {image_path}. Usá PNG o JPEG.")

    with open(path, "rb") as f:
        header = f.read(4)
    if not header.startswith(MAGIC_BYTES[mime_type]):
        raise ImageParsingError(f"{image_path} no es un {mime_type} válido (archivo corrupto o renombrado).")

    return mime_type


def encode_image(image_path: str) -> str:
    """Lee la imagen en binario y la convierte a texto base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_contract_image(image_path: str) -> str:
    """Transcribe una imagen de contrato a texto con GPT-4o Vision, respetando su jerarquía."""
    mime_type = validate_image(image_path)
    base64_image = encode_image(image_path)

    settings = get_settings()
    client = OpenAI(
        api_key=settings.openai_api_key,
        timeout=settings.request_timeout,
        max_retries=settings.max_retries,
    )

    try:
        response = client.chat.completions.create(
            model=settings.vision_model,
            max_tokens=settings.vision_max_tokens,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": VISION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{base64_image}", "detail": "high"},
                        },
                    ],
                }
            ],
        )
    except APITimeoutError as e:
        raise ImageParsingError(f"Timeout de OpenAI al leer {image_path}.") from e
    except RateLimitError as e:
        raise ImageParsingError("Límite de uso de OpenAI alcanzado (rate limit o sin crédito).") from e
    except APIConnectionError as e:
        raise ImageParsingError("No se pudo conectar con OpenAI. Revisá tu conexión.") from e
    except BadRequestError as e:
        raise ImageParsingError(f"OpenAI rechazó la imagen {image_path}: {e.message}") from e

    choice = response.choices[0]
    if choice.finish_reason == "length":
        raise ImageParsingError(
            f"La transcripción de {image_path} se cortó por límite de tokens. Subí VISION_MAX_TOKENS."
        )

    text = (choice.message.content or "").strip()
    if not text:
        raise ImageParsingError(f"GPT-4o no devolvió texto para {image_path}.")
    return text
