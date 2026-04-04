"""Erreur de base pour une incohérence détectée pendant un import catalogue."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class CatalogImportInconsistencyError(BaobabMtgCatalogException):
    """Données normalisées en contradiction avec le référentiel ou le lot courant.

    Les sous-classes précisent la nature du conflit (set, lot, lien printing).
    """
