"""Erreur de validation pour un numéro de collection invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCollectorNumberError(InvalidDomainValueError):
    """Levée lorsqu'un collector number est vide ou mal formé."""
