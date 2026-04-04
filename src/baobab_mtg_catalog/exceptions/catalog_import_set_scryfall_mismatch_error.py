"""Même code d'extension mais identifiant Scryfall du set différent."""

from baobab_mtg_catalog.exceptions.catalog_import_inconsistency_error import (
    CatalogImportInconsistencyError,
)


class CatalogImportSetScryfallMismatchError(CatalogImportInconsistencyError):
    """Un set déjà stocké sous le même code possède un autre ``scryfall_set_id`` que le payload."""
