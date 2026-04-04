"""Erreur de validation pour un coût de mana syntaxiquement invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidManaCostError(InvalidDomainValueError):
    """Levée lorsque la représentation textuelle du coût de mana est invalide."""
