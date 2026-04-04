"""Consultation métier des impressions (:class:`CardPrinting`)."""

from __future__ import annotations

from dataclasses import replace

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.repositories.card_printing_repository import (
    CardPrintingRepository,
    PrintingNaturalKey,
)
from baobab_mtg_catalog.services.catalog_definition_filter import CatalogDefinitionFilter
from baobab_mtg_catalog.services.catalog_printing_filter import CatalogPrintingFilter
from baobab_mtg_catalog.services.catalog_query_service import CatalogQueryService


class CardPrintingQueryService:
    """Lectures et listes sur les printings, y compris filtres métier combinés.

    :meth:`find` délègue à :class:`CatalogQueryService` pour les critères avancés
    (set, collector, rareté, sous-filtre définition, etc.).

    :param printing_repository: Source des impressions.
    :param catalog_query_service: Couche de filtrage catalogue partagée.
    """

    def __init__(
        self,
        *,
        printing_repository: CardPrintingRepository,
        catalog_query_service: CatalogQueryService,
    ) -> None:
        """Attache les dépendances de consultation."""
        self._printings = printing_repository
        self._catalog = catalog_query_service

    def get_by_id(self, printing_id: CardPrintingIdentifier) -> CardPrinting:
        """Retourne un printing par identifiant métier.

        :param printing_id: UUID métier.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent.
        """
        return self._printings.get_by_id(printing_id)

    def get_by_scryfall_printing_id(self, scryfall_printing_id: ScryfallId) -> CardPrinting:
        """Retourne un printing par UUID Scryfall de la carte (printing).

        :param scryfall_printing_id: Id Scryfall carte.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent ou non indexé.
        """
        return self._printings.get_by_scryfall_printing_id(scryfall_printing_id)

    def get_by_natural_key(self, key: PrintingNaturalKey) -> CardPrinting:
        """Retourne un printing par :meth:`CardPrinting.natural_key`.

        :param key: ``ScryfallId`` ou triplet ``(set_id, collector, langue)``.
        :returns: Printing trouvé.
        :raises CardPrintingNotFoundError: Si absent.
        """
        return self._printings.get_by_natural_key(key)

    def list_for_definition(
        self, definition_id: CardDefinitionIdentifier
    ) -> tuple[CardPrinting, ...]:
        """Liste toutes les impressions d'une carte logique.

        :param definition_id: Identifiant métier Oracle.
        :returns: Printings triés par ``CardPrintingIdentifier``.
        """
        return self._catalog.find_printings(
            CatalogPrintingFilter(
                definition=CatalogDefinitionFilter(card_definition_id=definition_id),
            ),
        )

    def list_for_set(self, set_id: SetId) -> tuple[CardPrinting, ...]:
        """Liste les impressions d'une extension.

        :param set_id: Identifiant métier du set.
        :returns: Printings du set (ordre du repository).
        """
        return self._printings.list_by_set_id(set_id)

    def find_in_set(
        self,
        set_id: SetId,
        filt: CatalogPrintingFilter,
    ) -> tuple[CardPrinting, ...]:
        """Filtre les printings d'un set selon des critères métier.

        ``set_id`` est appliqué en plus des champs non nuls de ``filt`` (ET).
        Le code set éventuel de ``filt`` est effacé pour éviter toute ambiguïté.

        :param set_id: Extension à restreindre.
        :param filt: Critères sur l'impression et optionnellement la définition.
        :returns: Printings satisfaisant l'intersection des critères.
        """
        merged = replace(filt, set_id=set_id, set_code=None)
        return self._catalog.find_printings(merged)

    def find(self, filt: CatalogPrintingFilter) -> tuple[CardPrinting, ...]:
        """Recherche d'impressions avec filtres combinés (ET).

        :param filt: Critères catalogue ; voir :class:`CatalogPrintingFilter`.
        :returns: Printings triés par identifiant métier.
        """
        return self._catalog.find_printings(filt)
