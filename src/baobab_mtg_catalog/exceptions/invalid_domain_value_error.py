"""Erreur de base pour les échecs de validation des objets de valeur du domaine."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class InvalidDomainValueError(BaobabMtgCatalogException):
    """Levée lorsqu'une valeur ne respecte pas les invariants d'un objet métier.

    Les erreurs plus spécifiques du domaine catalogue héritent généralement de
    cette classe pour permettre un     filtrage commun tout en gardant des types
    explicites.

    :param message: Description humaine du problème de validation.
    :type message: str
    """
