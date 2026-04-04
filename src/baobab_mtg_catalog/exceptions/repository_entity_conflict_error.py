"""Levée lorsqu'un enregistrement viole une contrainte d'unicité du référentiel."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class RepositoryEntityConflictError(BaobabMtgCatalogException):
    """Clé naturelle ou identifiant externe déjà associé à une autre entité métier."""
