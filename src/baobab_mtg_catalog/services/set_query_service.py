"""Consultation métier des extensions (:class:`~baobab_mtg_catalog.domain.sets.set.Set`)."""

from __future__ import annotations

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.repositories.set_repository import SetRepository


class SetQueryService:
    """Lectures orientées métier sur un :class:`SetRepository`.

    Délègue aux méthodes du repository ; aucune logique de filtrage avancé
    (voir :class:`CatalogQueryService` pour les prédicats combinés).

    :param set_repository: Source des extensions.
    """

    def __init__(self, *, set_repository: SetRepository) -> None:
        """Attache le repository consulté."""
        self._sets = set_repository

    def get_by_id(self, set_id: SetId) -> Set:
        """Retourne un set par identifiant métier.

        :param set_id: UUID métier de l'extension.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent.
        """
        return self._sets.get_by_id(set_id)

    def get_by_code(self, code: SetCode) -> Set:
        """Retourne un set par code d'extension (clé naturelle).

        :param code: Code Wizards / Scryfall.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent.
        """
        return self._sets.get_by_code(code)

    def get_by_scryfall_set_id(self, scryfall_set_id: ScryfallId) -> Set:
        """Retourne un set par identifiant Scryfall du produit extension.

        :param scryfall_set_id: UUID Scryfall du set.
        :returns: Set trouvé.
        :raises SetNotFoundError: Si absent ou non indexé.
        """
        return self._sets.get_by_scryfall_set_id(scryfall_set_id)

    def list_all(self) -> tuple[Set, ...]:
        """Liste toutes les extensions (ordre déterministe du repository).

        :returns: Séquence immuable.
        """
        return self._sets.list_all()
