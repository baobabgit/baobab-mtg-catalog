"""Levée lorsqu'un set catalogue est introuvable dans le référentiel."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class SetNotFoundError(BaobabMtgCatalogException):
    """Aucun :class:`~baobab_mtg_catalog.domain.sets.set.Set` ne correspond à la requête."""
