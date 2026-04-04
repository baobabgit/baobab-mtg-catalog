"""Erreur de validation pour un identifiant Gatherer / Multiverse."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidMultiverseIdError(InvalidDomainValueError):
    """Levée lorsqu'un multiverse id n'est pas un entier strictement positif."""
