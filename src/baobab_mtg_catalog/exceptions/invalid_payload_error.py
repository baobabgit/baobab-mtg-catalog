"""Erreur pour un payload Scryfall structurellement invalide ou incomplet."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class InvalidPayloadError(BaobabMtgCatalogException):
    """Levée lorsque le JSON Scryfall ne respecte pas la forme minimale attendue."""
