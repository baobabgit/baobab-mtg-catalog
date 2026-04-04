"""Champ ``set`` de la carte différent du set du lot importé."""

from baobab_mtg_catalog.exceptions.catalog_import_inconsistency_error import (
    CatalogImportInconsistencyError,
)


class CatalogImportBatchSetMismatchError(CatalogImportInconsistencyError):
    """Le code d'extension porté par la carte Scryfall ne correspond pas au set du lot."""
