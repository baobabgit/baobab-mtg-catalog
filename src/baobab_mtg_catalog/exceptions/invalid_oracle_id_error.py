"""Erreur de validation pour un oracle id métier."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidOracleIdError(InvalidDomainValueError):
    """Levée lorsqu'un oracle id (carte logique) est absent ou mal formé."""
