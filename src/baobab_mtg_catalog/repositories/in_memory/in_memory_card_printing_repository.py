"""Implémentation en mémoire de :class:`CardPrintingRepository`."""

from __future__ import annotations

from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions.card_printing_not_found_error import (
    CardPrintingNotFoundError,
)
from baobab_mtg_catalog.exceptions.repository_entity_conflict_error import (
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.repositories.card_printing_repository import (
    CardPrintingRepository,
    PrintingNaturalKey,
)


def _natural_key_tuple(key: PrintingNaturalKey) -> tuple[str, ...]:
    if isinstance(key, ScryfallId):
        return ("s", key.value)
    set_id, collector, language = key
    return ("l", set_id.value, collector.value, language.value)


class InMemoryCardPrintingRepository(CardPrintingRepository):
    """Stockage volatile des printings avec index par clé naturelle."""

    def __init__(self) -> None:
        """Initialise des tables vides."""
        self._by_id: dict[str, CardPrinting] = {}
        self._by_natural: dict[tuple[str, ...], CardPrinting] = {}
        self._by_scry_printing: dict[str, CardPrinting] = {}

    def upsert(self, printing: CardPrinting) -> CardPrinting:
        pid = printing.card_printing_id.value
        nk = printing.natural_key()
        nk_t = _natural_key_tuple(nk)

        at_nk = self._by_natural.get(nk_t)
        if at_nk is not None and at_nk.card_printing_id.value != pid:
            raise RepositoryEntityConflictError(
                "La clé naturelle du printing est déjà associée à un autre CardPrintingIdentifier."
            )

        if isinstance(nk, ScryfallId):
            at_s = self._by_scry_printing.get(nk.value)
            if at_s is not None and at_s.card_printing_id.value != pid:
                raise RepositoryEntityConflictError(
                    "L'identifiant Scryfall du printing est déjà associé à un autre id métier."
                )

        prev = self._by_id.get(pid)
        if prev is not None:
            prev_nk = prev.natural_key()
            del self._by_natural[_natural_key_tuple(prev_nk)]
            if isinstance(prev_nk, ScryfallId):
                self._by_scry_printing.pop(prev_nk.value, None)

        self._by_id[pid] = printing
        self._by_natural[nk_t] = printing
        if isinstance(nk, ScryfallId):
            self._by_scry_printing[nk.value] = printing
        return printing

    def get_by_id(self, printing_id: CardPrintingIdentifier) -> CardPrinting:
        found = self._by_id.get(printing_id.value)
        if found is None:
            raise CardPrintingNotFoundError(
                f"Aucun printing pour CardPrintingIdentifier {printing_id.value!r}."
            )
        return found

    def get_by_natural_key(self, key: PrintingNaturalKey) -> CardPrinting:
        found = self._by_natural.get(_natural_key_tuple(key))
        if found is None:
            raise CardPrintingNotFoundError("Aucun printing pour la clé naturelle fournie.")
        return found

    def get_by_scryfall_printing_id(self, scryfall_printing_id: ScryfallId) -> CardPrinting:
        found = self._by_scry_printing.get(scryfall_printing_id.value)
        if found is None:
            raise CardPrintingNotFoundError(
                f"Aucun printing pour l'id Scryfall {scryfall_printing_id.value!r}."
            )
        return found

    def list_by_set_id(self, set_id: SetId) -> tuple[CardPrinting, ...]:
        sid = set_id.value
        items = [p for p in self._by_id.values() if p.set_id.value == sid]
        items.sort(key=lambda p: p.card_printing_id.value)
        return tuple(items)

    def list_by_set_and_collector(
        self,
        set_id: SetId,
        collector_number: CollectorNumber,
    ) -> tuple[CardPrinting, ...]:
        sid = set_id.value
        cn = collector_number.value
        items = [
            p
            for p in self._by_id.values()
            if p.set_id.value == sid and p.collector_number.value == cn
        ]
        items.sort(key=lambda p: p.card_printing_id.value)
        return tuple(items)

    def list_all(self) -> tuple[CardPrinting, ...]:
        return tuple(p for _, p in sorted(self._by_id.items(), key=lambda kv: kv[0]))
