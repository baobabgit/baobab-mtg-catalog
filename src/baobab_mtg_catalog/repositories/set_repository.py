"""Interface d'accès aux :class:`~baobab_mtg_catalog.domain.sets.set.Set`."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode


class SetRepository(ABC):
    """Contrat de persistance / consultation des extensions catalogue.

    L':meth:`upsert` applique les clés naturelles : un :class:`SetCode` et un
    ``scryfall_set_id`` optionnel ne peuvent référencer qu'un seul ``SetId``.
    """

    @abstractmethod
    def upsert(self, set_obj: Set) -> Set:
        """Insère ou met à jour un set (idempotent si même ``SetId`` / clés).

        :param set_obj: Extension à enregistrer.
        :returns: L'instance enregistrée.
        :raises RepositoryEntityConflictError: Si une clé est déjà liée à un autre id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, set_id: SetId) -> Set:
        """Retourne un set par identifiant métier.

        :param set_id: UUID métier.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: SetCode) -> Set:
        """Retourne un set par code d'extension (clé naturelle).

        :param code: Code Wizards.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_scryfall_set_id(self, scryfall_set_id: ScryfallId) -> Set:
        """Retourne un set par identifiant Scryfall du produit extension.

        :param scryfall_set_id: UUID Scryfall du set.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent ou sans correspondance indexée.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> tuple[Set, ...]:
        """Liste tous les sets (ordre déterministe imposé par l'implémentation).

        :returns: Séquence immuable de sets.
        """
        raise NotImplementedError
