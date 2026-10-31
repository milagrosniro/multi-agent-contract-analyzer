"""Entry point: recibe 2 paths de imágenes y ejecuta el pipeline completo."""

import argparse
import sys

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from src.agents.contextualization_agent import ContextualizationAgent
from src.agents.errors import AgentError
from src.agents.extraction_agent import ExtractionAgent
from src.image_parser import ImageParsingError, parse_contract_image, validate_image
from src.models import ContractChangeOutput


def run_stages(langfuse, tracing_handler, original_path: str, amendment_path: str) -> ContractChangeOutput:
    """Ejecuta las 4 etapas del pipeline, cada una en su propio span."""
    with langfuse.start_as_current_observation(
        name="parse_original_contract", input={"path": original_path}
    ) as span:
        original_text = parse_contract_image(original_path)
        span.update(output=original_text, metadata={"characters": len(original_text)})

    with langfuse.start_as_current_observation(
        name="parse_amendment_contract", input={"path": amendment_path}
    ) as span:
        amendment_text = parse_contract_image(amendment_path)
        span.update(output=amendment_text, metadata={"characters": len(amendment_text)})

    with langfuse.start_as_current_observation(
        name="contextualization_agent",
        as_type="agent",
        input={"original_text": original_text, "amendment_text": amendment_text},
    ) as span:
        context_map = ContextualizationAgent().run(original_text, amendment_text, callbacks=[tracing_handler])
        span.update(output=context_map)

    with langfuse.start_as_current_observation(
        name="extraction_agent",
        as_type="agent",
        input={"context_map": context_map},
    ) as span:
        result = ExtractionAgent().run(context_map, original_text, amendment_text, callbacks=[tracing_handler])
        span.update(output=result.model_dump())

    return result


def run_pipeline(original_path: str, amendment_path: str) -> ContractChangeOutput:
    """Parsea ambas imágenes, arma el mapa contextual y extrae los cambios."""
    # Valida las dos imágenes antes de la primera llamada paga a la API
    validate_image(original_path)
    validate_image(amendment_path)

    langfuse = get_client()
    # Captura automáticamente modelo, tokens y latencia de las llamadas de LangChain
    tracing_handler = CallbackHandler()

    with langfuse.start_as_current_observation(
        name="contract-analysis",
        input={"original_path": original_path, "amendment_path": amendment_path},
    ) as root_span:
        try:
            result = run_stages(langfuse, tracing_handler, original_path, amendment_path)
        except (ImageParsingError, AgentError, EnvironmentError) as e:
            root_span.update(level="ERROR", status_message=str(e))
            raise

        root_span.update(
            output=result.model_dump(),
            metadata={"sections_changed": len(result.sections_changed)},
        )

    return result


def main() -> int:
    # Evita tildes rotas en terminales de Windows que no usan UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Compara un contrato con su enmienda a partir de dos imágenes.")
    parser.add_argument("original", help="Imagen del contrato original (PNG o JPEG)")
    parser.add_argument("amendment", help="Imagen de la enmienda (PNG o JPEG)")
    args = parser.parse_args()

    try:
        result = run_pipeline(args.original, args.amendment)
    except (ImageParsingError, AgentError, EnvironmentError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        # El envío a Langfuse es en segundo plano: sin esto se perderían las últimas trazas
        get_client().flush()

    print(result.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
