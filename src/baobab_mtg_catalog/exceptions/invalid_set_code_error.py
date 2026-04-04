"""Erreur de validation pour un code d'extension (set) invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidSetCodeError(InvalidDomainValueError):
    """Levée lorsqu'un code de set ne respecte pas le format métier attendu."""
