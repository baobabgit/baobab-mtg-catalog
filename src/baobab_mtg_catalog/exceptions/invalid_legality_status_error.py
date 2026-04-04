"""Erreur de validation pour un statut de légalité inconnu."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidLegalityStatusError(InvalidDomainValueError):
    """Levée lorsqu'un statut de légalité ne correspond pas au référentiel."""
