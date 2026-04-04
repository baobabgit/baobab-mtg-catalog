"""Erreur de validation pour une ligne de type de carte invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardTypeLineError(InvalidDomainValueError):
    """Levée lorsque la ligne de types / sous-types est rejetée par le domaine."""
