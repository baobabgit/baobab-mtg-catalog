"""Erreur de validation pour une identité de couleur incohérente."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidColorIdentityError(InvalidDomainValueError):
    """Levée lorsque la construction d'une identité de couleur est invalide."""
