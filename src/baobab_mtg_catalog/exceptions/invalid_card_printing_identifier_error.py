"""Erreur de validation pour un identifiant métier de printing invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardPrintingIdentifierError(InvalidDomainValueError):
    """Levée lorsque l'UUID d'un printing catalogue est rejeté."""
