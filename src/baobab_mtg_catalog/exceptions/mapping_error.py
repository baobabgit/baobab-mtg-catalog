"""Erreur lors du mapping Scryfall vers le modèle métier local."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class MappingError(BaobabMtgCatalogException):
    """Levée lorsque la construction d'un objet de domaine depuis Scryfall échoue."""
