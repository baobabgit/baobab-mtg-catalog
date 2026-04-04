"""Erreur de validation pour une rareté inconnue."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidRarityError(InvalidDomainValueError):
    """Levée lorsqu'une rareté ne correspond pas aux valeurs métier supportées."""
