"""Consultation filtrée du catalogue à partir des repositories."""

from __future__ import annotations

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.exceptions import (
    CardPrintingNotFoundError,
)
from baobab_mtg_catalog.repositories.card_definition_repository import CardDefinitionRepository
from baobab_mtg_catalog.repositories.card_printing_repository import CardPrintingRepository
from baobab_mtg_catalog.repositories.set_repository import SetRepository
from baobab_mtg_catalog.services.catalog_definition_filter import CatalogDefinitionFilter
from baobab_mtg_catalog.services.catalog_printing_filter import CatalogPrintingFilter
from baobab_mtg_catalog.services.catalog_set_filter import CatalogSetFilter


def _norm_substring(raw: str | None) -> str | None:
    if raw is None:
        return None
    stripped = raw.strip().lower()
    return stripped if stripped else None


def _definition_matches(definition: CardDefinition, filt: CatalogDefinitionFilter) -> bool:
    ok = True
    if filt.card_definition_id is not None:
        ok = ok and definition.card_definition_id == filt.card_definition_id
    if filt.oracle_id is not None:
        ok = ok and definition.oracle_id == filt.oracle_id
    if filt.scryfall_card_id is not None:
        ok = ok and definition.scryfall_card_id == filt.scryfall_card_id
    if filt.multiverse_id is not None:
        ok = ok and definition.multiverse_id == filt.multiverse_id
    sub_name = _norm_substring(filt.normalized_name_contains)
    if sub_name is not None:
        ok = ok and sub_name in definition.normalized_name
    sub_tl = _norm_substring(filt.type_line_contains)
    if sub_tl is not None:
        ok = ok and sub_tl in definition.type_line.value.lower()
    if filt.any_of_colors is not None and len(filt.any_of_colors) > 0:
        ok = ok and bool(definition.colors & filt.any_of_colors)
    if filt.color_identity_within is not None:
        ok = ok and definition.color_identity.colors <= filt.color_identity_within.colors
    return ok


def _printing_matches(
    printing: CardPrinting,
    definition: CardDefinition,
    filt: CatalogPrintingFilter,
    *,
    effective_set_id: SetId | None,
) -> bool:
    ok = True
    if effective_set_id is not None:
        ok = ok and printing.set_id == effective_set_id
    if filt.collector_number is not None:
        ok = ok and printing.collector_number == filt.collector_number
    if filt.language is not None:
        ok = ok and printing.language == filt.language
    if filt.rarities is not None and len(filt.rarities) > 0:
        ok = ok and printing.rarity in filt.rarities
    if filt.scryfall_printing_id is not None:
        spid = printing.scryfall_printing_id
        ok = ok and spid is not None and spid.value == filt.scryfall_printing_id.value
    if filt.multiverse_id is not None:
        pm = printing.multiverse_id == filt.multiverse_id
        dm = definition.multiverse_id == filt.multiverse_id
        ok = ok and (pm or dm)
    if filt.definition is not None:
        ok = ok and _definition_matches(definition, filt.definition)
    return ok


def _set_matches(set_obj: Set, filt: CatalogSetFilter) -> bool:
    ok = True
    if filt.set_id is not None:
        ok = ok and set_obj.set_id == filt.set_id
    if filt.set_code is not None:
        ok = ok and set_obj.code.value == filt.set_code.value
    if filt.set_type is not None:
        ok = ok and set_obj.set_type == filt.set_type
    if filt.scryfall_set_id is not None:
        ok = ok and set_obj.scryfall_set_id is not None
        if set_obj.scryfall_set_id is not None:
            ok = ok and set_obj.scryfall_set_id.value == filt.scryfall_set_id.value
    sub = _norm_substring(filt.name_contains)
    if sub is not None:
        ok = ok and sub in set_obj.name.lower()
    return ok


class CatalogQueryService:
    """Couche de lecture métier au-dessus des repositories (parcours en mémoire).

    Les filtres combinent leurs critères non nuls par un **ET** logique. Les
    résultats sont triés de façon déterministe (UUID métier croissant).

    La légalité de format n'est pas modélisée sur :class:`CardDefinition` dans
    cette version : aucun filtre de ce type n'est proposé ici.

    :param set_repository: Source des extensions.
    :param definition_repository: Source des définitions Oracle.
    :param printing_repository: Source des impressions.
    """

    def __init__(
        self,
        *,
        set_repository: SetRepository,
        definition_repository: CardDefinitionRepository,
        printing_repository: CardPrintingRepository,
    ) -> None:
        """Attache les repositories consultés."""
        self._sets = set_repository
        self._definitions = definition_repository
        self._printings = printing_repository

    def find_sets(self, filt: CatalogSetFilter) -> tuple[Set, ...]:
        """Liste les sets satisfaisant le filtre.

        :param filt: Critères ; champs ``None`` ignorés.
        :returns: Séquence triée par ``SetId``.
        """
        matched = [s for s in self._sets.list_all() if _set_matches(s, filt)]
        matched.sort(key=lambda s: s.set_id.value)
        return tuple(matched)

    def find_definitions(self, filt: CatalogDefinitionFilter) -> tuple[CardDefinition, ...]:
        """Liste les définitions Oracle satisfaisant le filtre.

        :param filt: Critères sur la définition seule.
        :returns: Séquence triée par ``CardDefinitionIdentifier``.
        """
        matched = [d for d in self._definitions.list_all() if _definition_matches(d, filt)]
        matched.sort(key=lambda d: d.card_definition_id.value)
        return tuple(matched)

    def find_printings(self, filt: CatalogPrintingFilter) -> tuple[CardPrinting, ...]:
        """Liste les impressions dont le printing et la définition liée satisfont le filtre.

        :param filt: Critères ; :attr:`CatalogPrintingFilter.set_code` inexistant
            lève :class:`SetNotFoundError` (aligné sur le repository).
        :returns: Séquence triée par ``CardPrintingIdentifier``.
        """
        if filt.card_printing_id is not None:
            try:
                printing = self._printings.get_by_id(filt.card_printing_id)
            except CardPrintingNotFoundError:
                return ()
            definition = self._definitions.get_by_id(printing.card_definition_id)
            eff, impossible = self._resolve_printing_set_scope(filt)
            if impossible:
                return ()
            if _printing_matches(printing, definition, filt, effective_set_id=eff):
                return (printing,)
            return ()

        eff, impossible = self._resolve_printing_set_scope(filt)
        if impossible:
            return ()

        candidates: tuple[CardPrinting, ...]
        if eff is not None and filt.collector_number is not None:
            candidates = self._printings.list_by_set_and_collector(eff, filt.collector_number)
        elif eff is not None:
            candidates = self._printings.list_by_set_id(eff)
        else:
            candidates = self._printings.list_all()

        out: list[CardPrinting] = []
        for printing in candidates:
            definition = self._definitions.get_by_id(printing.card_definition_id)
            if _printing_matches(printing, definition, filt, effective_set_id=eff):
                out.append(printing)
        out.sort(key=lambda p: p.card_printing_id.value)
        return tuple(out)

    def _resolve_printing_set_scope(
        self,
        filt: CatalogPrintingFilter,
    ) -> tuple[SetId | None, bool]:
        """Résout le set effectif et détecte code + id contradictoires."""
        if filt.set_code is not None:
            st = self._sets.get_by_code(filt.set_code)
            if filt.set_id is not None and filt.set_id != st.set_id:
                return None, True
            return st.set_id, False
        if filt.set_id is not None:
            return filt.set_id, False
        return None, False
