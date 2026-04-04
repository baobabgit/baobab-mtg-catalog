"""Critères de filtrage sur les définitions Oracle (sans contexte printing)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId


@dataclass(frozen=True, slots=True)
class CatalogDefinitionFilter:
    """Filtre ET sur une définition Oracle (``CardDefinition``).

    Les champs ``None`` sont ignorés.

    :param card_definition_id: Identifiant métier exact.
    :param oracle_id: Oracle id stable.
    :param scryfall_card_id: Id Scryfall carte (racine JSON carte).
    :param multiverse_id: Multiverse Gatherer sur la définition.
    :param normalized_name_contains: Sous-chaîne (casse ignorée) dans le nom normalisé.
    :param type_line_contains: Sous-chaîne (casse ignorée) dans la ligne de types.
    :param any_of_colors: Au moins une couleur commune avec la carte.
    :param color_identity_within: Identité carte ⊆ cette identité (ex. deck).
    """

    card_definition_id: CardDefinitionIdentifier | None = None
    oracle_id: OracleId | None = None
    scryfall_card_id: ScryfallId | None = None
    multiverse_id: MultiverseId | None = None
    normalized_name_contains: str | None = None
    type_line_contains: str | None = None
    any_of_colors: frozenset[Color] | None = None
    color_identity_within: ColorIdentity | None = None
