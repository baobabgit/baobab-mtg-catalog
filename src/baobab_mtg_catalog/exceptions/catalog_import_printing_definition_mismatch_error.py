"""Même impression (clé naturelle) déjà liée à une autre définition Oracle."""

from baobab_mtg_catalog.exceptions.catalog_import_inconsistency_error import (
    CatalogImportInconsistencyError,
)


class CatalogImportPrintingDefinitionMismatchError(CatalogImportInconsistencyError):
    """Printing existant : même clé naturelle, lien définition ou set métier différent."""
