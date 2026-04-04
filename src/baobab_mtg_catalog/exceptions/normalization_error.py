"""Erreur lors de la normalisation sémantique de données Scryfall."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class NormalizationError(BaobabMtgCatalogException):
    """Levée lorsqu'une valeur Scryfall est ambiguë ou incohérente après normalisation."""
