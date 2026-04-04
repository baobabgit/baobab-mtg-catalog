"""Levée lorsqu'un printing catalogue est introuvable dans le référentiel."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class CardPrintingNotFoundError(BaobabMtgCatalogException):
    """Aucune impression catalogue ne correspond à la requête."""
