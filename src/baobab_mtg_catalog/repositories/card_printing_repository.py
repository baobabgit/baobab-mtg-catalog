"""Contrat de persistance pour les impressions catalogue (entité ``CardPrinting``)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeAlias

from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId

PrintingNaturalKey: TypeAlias = ScryfallId | tuple[SetId, CollectorNumber, Language]


class CardPrintingRepository(ABC):
    """Contrat de persistance / consultation des impressions.

    L':meth:`upsert` aligne les index sur :meth:`CardPrinting.natural_key` et
    interdit les collisions entre identifiants métier distincts.
    """

    @abstractmethod
    def upsert(self, printing: CardPrinting) -> CardPrinting:
        """Insère ou met à jour un printing.

        :param printing: Impression à enregistrer.
        :returns: L'instance enregistrée.
        :raises RepositoryEntityConflictError: Si une clé naturelle / Scryfall entre en conflit.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, printing_id: CardPrintingIdentifier) -> CardPrinting:
        """Retourne un printing par identifiant métier.

        :param printing_id: UUID métier.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_natural_key(self, key: PrintingNaturalKey) -> CardPrinting:
        """Retourne un printing par clé naturelle (:meth:`CardPrinting.natural_key`).

        :param key: ``ScryfallId`` ou triplet de repli.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_scryfall_printing_id(self, scryfall_printing_id: ScryfallId) -> CardPrinting:
        """Retourne un printing par identifiant Scryfall carte (printing).

        :param scryfall_printing_id: UUID Scryfall.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent ou non indexé.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_set_id(self, set_id: SetId) -> tuple[CardPrinting, ...]:
        """Liste les printings dont le set métier correspond.

        :param set_id: Identifiant d'extension.
        :returns: Séquence immuable, ordre déterministe.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_set_and_collector(
        self,
        set_id: SetId,
        collector_number: CollectorNumber,
    ) -> tuple[CardPrinting, ...]:
        """Liste les printings pour un set et un numéro de collection donnés.

        :param set_id: Identifiant d'extension.
        :param collector_number: Numéro de collection.
        :returns: Séquence immuable, ordre déterministe.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> tuple[CardPrinting, ...]:
        """Liste tous les printings (ordre déterministe).

        :returns: Séquence immuable.
        """
        raise NotImplementedError
