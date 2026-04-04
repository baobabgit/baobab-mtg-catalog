"""Adaptateurs Scryfall → modèle métier catalogue."""

from baobab_mtg_catalog.adapters.scryfall.scryfall_card_definition_adapter import (
    ScryfallCardDefinitionAdapter,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_card_printing_adapter import (
    ScryfallCardPrintingAdapter,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_set_adapter import ScryfallSetAdapter

__all__: list[str] = [
    "ScryfallCardDefinitionAdapter",
    "ScryfallCardPrintingAdapter",
    "ScryfallSetAdapter",
]
