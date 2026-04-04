"""Consultation métier des cartes logiques (:class:`CardDefinition`)."""

from __future__ import annotations

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.repositories.card_definition_repository import CardDefinitionRepository
from baobab_mtg_catalog.repositories.card_printing_repository import CardPrintingRepository
from baobab_mtg_catalog.services.catalog_definition_filter import CatalogDefinitionFilter
from baobab_mtg_catalog.services.catalog_query_service import CatalogQueryService


class CardDefinitionQueryService:
    """Accès et listes courantes sur les définitions Oracle.

    Les recherches par fragment de nom délèguent à :class:`CatalogQueryService`
    pour réutiliser les mêmes règles que les filtres catalogue.

    :param definition_repository: Source des définitions.
    :param printing_repository: Utilisé pour les définitions présentes dans un set.
    :param catalog_query_service: Requêtes filtrées (nom, types, couleurs, etc.).
    """

    def __init__(
        self,
        *,
        definition_repository: CardDefinitionRepository,
        printing_repository: CardPrintingRepository,
        catalog_query_service: CatalogQueryService,
    ) -> None:
        """Attache les dépendances de consultation."""
        self._definitions = definition_repository
        self._printings = printing_repository
        self._catalog = catalog_query_service

    def get_by_id(self, definition_id: CardDefinitionIdentifier) -> CardDefinition:
        """Retourne une carte logique par identifiant métier.

        :param definition_id: UUID métier Oracle.
        :returns: Définition trouvée.
        :raises CardDefinitionNotFoundError: Si absent.
        """
        return self._definitions.get_by_id(definition_id)

    def get_by_oracle_id(self, oracle_id: OracleId) -> CardDefinition:
        """Retourne une carte logique par oracle id (clé naturelle).

        :param oracle_id: Identifiant oracle stable.
        :returns: Définition trouvée.
        :raises CardDefinitionNotFoundError: Si absent.
        """
        return self._definitions.get_by_oracle_id(oracle_id)

    def list_by_normalized_name(self, normalized_name: str) -> tuple[CardDefinition, ...]:
        """Liste les définitions dont :attr:`CardDefinition.normalized_name` est égal.

        :param normalized_name: Nom déjà normalisé (ex. minuscules).
        :returns: Séquence immuable, ordre déterministe.
        """
        return self._definitions.list_by_normalized_name(normalized_name)

    def find_by_name_contains(self, fragment: str) -> tuple[CardDefinition, ...]:
        """Liste les définitions dont le nom normalisé contient ``fragment`` (sans casse).

        :param fragment: Sous-chaîne recherchée (espaces de bord ignorés).
        :returns: Définitions triées par identifiant métier.
        """
        return self._catalog.find_definitions(
            CatalogDefinitionFilter(normalized_name_contains=fragment),
        )

    def list_for_set(self, set_id: SetId) -> tuple[CardDefinition, ...]:
        """Liste les cartes logiques ayant au moins un printing dans l'extension.

        Chaque :class:`CardDefinition` n'apparaît qu'une fois ; ordre par id métier.

        :param set_id: Extension cible.
        :returns: Définitions distinctes liées aux printings du set.
        """
        printings = self._printings.list_by_set_id(set_id)
        seen: set[str] = set()
        out: list[CardDefinition] = []
        for printing in printings:
            did = printing.card_definition_id.value
            if did in seen:
                continue
            seen.add(did)
            out.append(self._definitions.get_by_id(printing.card_definition_id))
        out.sort(key=lambda d: d.card_definition_id.value)
        return tuple(out)
