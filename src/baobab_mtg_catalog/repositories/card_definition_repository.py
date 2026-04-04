"""Contrat de persistance pour les cartes Oracle (entité ``CardDefinition``)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId


class CardDefinitionRepository(ABC):
    """Contrat de persistance / consultation des définitions Oracle.

    L':meth:`upsert` garantit l'unicité de l':class:`OracleId` (clé naturelle)
    pour un :class:`CardDefinitionIdentifier` donné.
    """

    @abstractmethod
    def upsert(self, definition: CardDefinition) -> CardDefinition:
        """Insère ou met à jour une définition.

        :param definition: Carte logique à enregistrer.
        :returns: L'instance enregistrée.
        :raises RepositoryEntityConflictError: Si l'oracle id est déjà lié à un autre id métier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, definition_id: CardDefinitionIdentifier) -> CardDefinition:
        """Retourne une définition par identifiant métier.

        :param definition_id: UUID métier.
        :returns: Définition trouvée.
        :raises CardDefinitionNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_oracle_id(self, oracle_id: OracleId) -> CardDefinition:
        """Retourne une définition par oracle id (clé naturelle).

        :param oracle_id: Identifiant oracle stable.
        :returns: Définition trouvée.
        :raises CardDefinitionNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_normalized_name(self, normalized_name: str) -> tuple[CardDefinition, ...]:
        """Filtre simple sur :attr:`CardDefinition.normalized_name` (égalité exacte).

        :param normalized_name: Nom déjà normalisé (ex. minuscules).
        :returns: Séquence immuable, ordre déterministe.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> tuple[CardDefinition, ...]:
        """Liste toutes les définitions (ordre déterministe).

        :returns: Séquence immuable.
        """
        raise NotImplementedError
