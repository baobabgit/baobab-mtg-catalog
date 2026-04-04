"""Implémentation en mémoire de :class:`CardDefinitionRepository`."""

from __future__ import annotations

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.exceptions.card_definition_not_found_error import (
    CardDefinitionNotFoundError,
)
from baobab_mtg_catalog.exceptions.repository_entity_conflict_error import (
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.repositories.card_definition_repository import (
    CardDefinitionRepository,
)


class InMemoryCardDefinitionRepository(CardDefinitionRepository):
    """Stockage volatile des définitions avec index par oracle id."""

    def __init__(self) -> None:
        """Initialise des tables vides."""
        self._by_id: dict[str, CardDefinition] = {}
        self._by_oracle: dict[str, CardDefinition] = {}

    def upsert(self, definition: CardDefinition) -> CardDefinition:
        cid = definition.card_definition_id.value
        ok = definition.natural_key().value

        at_oracle = self._by_oracle.get(ok)
        if at_oracle is not None and at_oracle.card_definition_id.value != cid:
            raise RepositoryEntityConflictError(
                f"L'oracle id {ok!r} est déjà associé à un autre CardDefinitionIdentifier."
            )

        prev = self._by_id.get(cid)
        if prev is not None and prev.oracle_id.value != ok:
            del self._by_oracle[prev.oracle_id.value]

        self._by_id[cid] = definition
        self._by_oracle[ok] = definition
        return definition

    def get_by_id(self, definition_id: CardDefinitionIdentifier) -> CardDefinition:
        found = self._by_id.get(definition_id.value)
        if found is None:
            raise CardDefinitionNotFoundError(
                f"Aucune définition pour CardDefinitionIdentifier {definition_id.value!r}."
            )
        return found

    def get_by_oracle_id(self, oracle_id: OracleId) -> CardDefinition:
        found = self._by_oracle.get(oracle_id.value)
        if found is None:
            raise CardDefinitionNotFoundError(
                f"Aucune définition pour l'oracle id {oracle_id.value!r}."
            )
        return found

    def list_by_normalized_name(self, normalized_name: str) -> tuple[CardDefinition, ...]:
        matches = [d for d in self._by_id.values() if d.normalized_name == normalized_name]
        matches.sort(key=lambda d: d.card_definition_id.value)
        return tuple(matches)

    def list_all(self) -> tuple[CardDefinition, ...]:
        return tuple(d for _, d in sorted(self._by_id.items(), key=lambda kv: kv[0]))
