"""Critères de filtrage sur les extensions catalogue."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode


@dataclass(frozen=True, slots=True)
class CatalogSetFilter:
    """Filtre combiné (ET logique) sur :class:`~baobab_mtg_catalog.domain.sets.set.Set`.

    Les champs ``None`` sont ignorés.

    :param set_id: Identifiant métier exact.
    :param set_code: Code d'extension exact.
    :param name_contains: Sous-chaîne (insensible à la casse) dans le nom du set.
    :param set_type: Type de produit extension.
    :param scryfall_set_id: Identifiant Scryfall du produit set.
    """

    set_id: SetId | None = None
    set_code: SetCode | None = None
    name_contains: str | None = None
    set_type: SetType | None = None
    scryfall_set_id: ScryfallId | None = None
