"""Implémentation en mémoire de :class:`SetRepository`."""

from __future__ import annotations

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions.repository_entity_conflict_error import (
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.exceptions.set_not_found_error import SetNotFoundError
from baobab_mtg_catalog.repositories.set_repository import SetRepository


class InMemorySetRepository(SetRepository):
    """Stockage volatile des sets avec index par code et Scryfall."""

    def __init__(self) -> None:
        """Initialise des tables vides."""
        self._by_id: dict[str, Set] = {}
        self._by_code: dict[str, Set] = {}
        self._by_scryfall: dict[str, Set] = {}

    def upsert(self, set_obj: Set) -> Set:
        oid = set_obj.set_id.value
        code_key = set_obj.natural_key().value

        at_code = self._by_code.get(code_key)
        if at_code is not None and at_code.set_id.value != oid:
            raise RepositoryEntityConflictError(
                f"Le code de set {code_key!r} est déjà associé à un autre SetId."
            )

        if set_obj.scryfall_set_id is not None:
            sid = set_obj.scryfall_set_id.value
            at_s = self._by_scryfall.get(sid)
            if at_s is not None and at_s.set_id.value != oid:
                raise RepositoryEntityConflictError(
                    "L'identifiant Scryfall du set est déjà associé à un autre SetId."
                )

        prev = self._by_id.get(oid)
        if prev is not None:
            if prev.natural_key().value != code_key:
                del self._by_code[prev.natural_key().value]
            if prev.scryfall_set_id is not None:
                ps = prev.scryfall_set_id.value
                if self._by_scryfall.get(ps) is prev:
                    del self._by_scryfall[ps]

        self._by_id[oid] = set_obj
        self._by_code[code_key] = set_obj
        if set_obj.scryfall_set_id is not None:
            self._by_scryfall[set_obj.scryfall_set_id.value] = set_obj
        return set_obj

    def get_by_id(self, set_id: SetId) -> Set:
        found = self._by_id.get(set_id.value)
        if found is None:
            raise SetNotFoundError(f"Aucun set pour SetId {set_id.value!r}.")
        return found

    def get_by_code(self, code: SetCode) -> Set:
        found = self._by_code.get(code.value)
        if found is None:
            raise SetNotFoundError(f"Aucun set pour le code {code.value!r}.")
        return found

    def get_by_scryfall_set_id(self, scryfall_set_id: ScryfallId) -> Set:
        found = self._by_scryfall.get(scryfall_set_id.value)
        if found is None:
            raise SetNotFoundError(
                f"Aucun set pour l'identifiant Scryfall {scryfall_set_id.value!r}."
            )
        return found

    def list_all(self) -> tuple[Set, ...]:
        return tuple(s for _, s in sorted(self._by_id.items(), key=lambda kv: kv[0]))
