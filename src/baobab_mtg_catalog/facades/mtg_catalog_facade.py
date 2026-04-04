"""Façade publique de haut niveau pour consommer le référentiel catalogue."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from baobab_mtg_catalog.repositories.card_definition_repository import CardDefinitionRepository
from baobab_mtg_catalog.repositories.card_printing_repository import CardPrintingRepository
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_definition_repository import (
    InMemoryCardDefinitionRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_printing_repository import (
    InMemoryCardPrintingRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_set_repository import (
    InMemorySetRepository,
)
from baobab_mtg_catalog.repositories.set_repository import SetRepository
from baobab_mtg_catalog.services.card_definition_query_service import CardDefinitionQueryService
from baobab_mtg_catalog.services.card_printing_query_service import CardPrintingQueryService
from baobab_mtg_catalog.services.catalog_import_batch_result import CatalogImportBatchResult
from baobab_mtg_catalog.services.catalog_import_service import CatalogImportService
from baobab_mtg_catalog.services.catalog_query_service import CatalogQueryService
from baobab_mtg_catalog.services.set_query_service import SetQueryService


class MtgCatalogFacade:
    """Point d'entrée stable pour les autres briques Baobab.

    Regroupe import idempotent, consultation par entité et requêtes filtrées sans
    exposer le câblage interne des repositories. Les consommateurs peuvent
    injecter leurs propres implémentations de repositories ou utiliser
    :meth:`in_memory` pour un référentiel volatile prêt à l'emploi.

    :param set_repository: Persistance / consultation des extensions.
    :param definition_repository: Persistance / consultation des définitions Oracle.
    :param printing_repository: Persistance / consultation des impressions.
    """

    def __init__(
        self,
        *,
        set_repository: SetRepository,
        definition_repository: CardDefinitionRepository,
        printing_repository: CardPrintingRepository,
    ) -> None:
        """Construit les services à partir des repositories fournis."""
        self._set_repository = set_repository
        self._definition_repository = definition_repository
        self._printing_repository = printing_repository
        self._catalog_query = CatalogQueryService(
            set_repository=set_repository,
            definition_repository=definition_repository,
            printing_repository=printing_repository,
        )
        self._import_service = CatalogImportService(
            set_repository=set_repository,
            definition_repository=definition_repository,
            printing_repository=printing_repository,
        )
        self._set_queries = SetQueryService(set_repository=set_repository)
        self._definition_queries = CardDefinitionQueryService(
            definition_repository=definition_repository,
            printing_repository=printing_repository,
            catalog_query_service=self._catalog_query,
        )
        self._printing_queries = CardPrintingQueryService(
            printing_repository=printing_repository,
            catalog_query_service=self._catalog_query,
        )

    @classmethod
    def in_memory(cls) -> MtgCatalogFacade:
        """Fabrique une façade branchée sur des repositories in-memory vides.

        :returns: Façade prête pour import et consultation en processus.
        """
        return cls(
            set_repository=InMemorySetRepository(),
            definition_repository=InMemoryCardDefinitionRepository(),
            printing_repository=InMemoryCardPrintingRepository(),
        )

    @property
    def sets(self) -> SetQueryService:
        """Consultation des extensions (get par id / code / Scryfall, liste)."""
        return self._set_queries

    @property
    def definitions(self) -> CardDefinitionQueryService:
        """Consultation des cartes logiques (get, nom exact ou fragment, par set)."""
        return self._definition_queries

    @property
    def printings(self) -> CardPrintingQueryService:
        """Consultation des impressions (get, listes par carte ou set, filtres)."""
        return self._printing_queries

    @property
    def catalog(self) -> CatalogQueryService:
        """Requêtes catalogue à filtres combinés (sets, définitions, printings)."""
        return self._catalog_query

    @property
    def importer(self) -> CatalogImportService:
        """Import idempotent Scryfall → référentiel (payloads ``Mapping``)."""
        return self._import_service

    def import_set_and_cards(
        self,
        set_payload: Mapping[str, Any],
        card_payloads: Sequence[Mapping[str, Any]],
    ) -> CatalogImportBatchResult:
        """Raccourci vers :meth:`CatalogImportService.import_set_and_cards`.

        :param set_payload: JSON Scryfall ``set``.
        :param card_payloads: Cartes du même produit extension.
        :returns: Set enregistré et nombre de cartes traitées.
        """
        return self._import_service.import_set_and_cards(set_payload, card_payloads)
