"""Accès persistant ou en mémoire au référentiel catalogue."""

from baobab_mtg_catalog.repositories.card_definition_repository import (
    CardDefinitionRepository,
)
from baobab_mtg_catalog.repositories.card_printing_repository import (
    CardPrintingRepository,
    PrintingNaturalKey,
)
from baobab_mtg_catalog.repositories.in_memory import (
    InMemoryCardDefinitionRepository,
    InMemoryCardPrintingRepository,
    InMemorySetRepository,
)
from baobab_mtg_catalog.repositories.set_repository import SetRepository

__all__: list[str] = [
    "CardDefinitionRepository",
    "CardPrintingRepository",
    "InMemoryCardDefinitionRepository",
    "InMemoryCardPrintingRepository",
    "InMemorySetRepository",
    "PrintingNaturalKey",
    "SetRepository",
]
