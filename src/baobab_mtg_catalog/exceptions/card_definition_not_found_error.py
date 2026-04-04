"""Levée lorsqu'une définition de carte est introuvable dans le référentiel."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class CardDefinitionNotFoundError(BaobabMtgCatalogException):
    """Aucune définition Oracle ne correspond à la requête."""
