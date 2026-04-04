"""Critères de filtrage sur les impressions et, optionnellement, la définition liée."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services.catalog_definition_filter import CatalogDefinitionFilter


@dataclass(frozen=True, slots=True)
class CatalogPrintingFilter:
    """Filtre ET sur une impression (``CardPrinting``) et optionnellement sa définition.

    Voir :attr:`definition` pour les critères Oracle.

    Si :attr:`set_id` et :attr:`set_code` sont tous deux renseignés, ils doivent
    désigner le même set ; sinon aucun printing ne correspond.

    :param set_id: Set métier de l'impression.
    :param set_code: Code d'extension (résolu via le repository des sets).
    :param collector_number: Numéro de collection exact.
    :param language: Langue de l'impression.
    :param rarities: L'impression doit avoir une rareté dans cet ensemble (OU interne).
    :param card_printing_id: Identifiant métier printing exact.
    :param scryfall_printing_id: Id Scryfall de la carte (printing).
    :param multiverse_id: Correspond si l'impression **ou** la définition porte cet id Gatherer.
    :param definition: Sous-filtre sur la définition référencée par l'impression.
    """

    set_id: SetId | None = None
    set_code: SetCode | None = None
    collector_number: CollectorNumber | None = None
    language: Language | None = None
    rarities: frozenset[Rarity] | None = None
    card_printing_id: CardPrintingIdentifier | None = None
    scryfall_printing_id: ScryfallId | None = None
    multiverse_id: MultiverseId | None = None
    definition: CatalogDefinitionFilter | None = None
