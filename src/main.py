"""Entry point: recibe 2 paths de imágenes y ejecuta el pipeline completo."""

import argparse
import sys

from src.agents.contextualization_agent import ContextualizationAgent
from src.agents.extraction_agent import ExtractionAgent, ExtractionError
from src.image_parser import ImageParsingError, parse_contract_image, validate_image
from src.models import ContractChangeOutput


def run_pipeline(original_path: str, amendment_path: str) -> ContractChangeOutput:
    """Parsea ambas imágenes, arma el mapa contextual y extrae los cambios."""
    # Valida las dos imágenes antes de la primera llamada paga a la API
    validate_image(original_path)
    validate_image(amendment_path)

    original_text = parse_contract_image(original_path)
    amendment_text = parse_contract_image(amendment_path)
    context_map = ContextualizationAgent().run(original_text, amendment_text)
    return ExtractionAgent().run(context_map, original_text, amendment_text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compara un contrato con su enmienda a partir de dos imágenes.")
    parser.add_argument("original", help="Imagen del contrato original (PNG o JPEG)")
    parser.add_argument("amendment", help="Imagen de la enmienda (PNG o JPEG)")
    args = parser.parse_args()

    try:
        result = run_pipeline(args.original, args.amendment)
    except (ImageParsingError, ExtractionError, EnvironmentError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(result.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
