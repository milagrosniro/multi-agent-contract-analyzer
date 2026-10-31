"""Pydantic models: ContractChangeOutput."""

from typing import List
from pydantic import BaseModel, Field, field_validator


class ContractChangeOutput(BaseModel):
    sections_changed: List[str] = Field(
        ...,
        description=(
            "Every clause or section that was added, removed or modified in the amendment, "
            "identified by its number and title exactly as written in the contract "
            "(e.g. '3. Honorarios'). Do not include unchanged sections."
        ),
    )
    topics_touched: List[str] = Field(
        ...,
        description=(
            "Legal or commercial topics affected by the changes, as short lowercase labels "
            "in Spanish (e.g. 'precio', 'plazo', 'confidencialidad'). No duplicates."
        ),
    )
    summary_of_the_change: str = Field(
        ...,
        description=(
            "Clear summary in Spanish of what changed, for each affected section: "
            "type of change (addition, removal or modification) and the before -> after values "
            "(e.g. 'Cláusula 3: el monto pasa de USD 2.500 a USD 2.800')."
        ),
    )

    @field_validator("summary_of_the_change")
    @classmethod
    def validate_summary_not_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("summary_of_the_change no puede estar vacío: el resumen debe describir los cambios.")
        return cleaned
