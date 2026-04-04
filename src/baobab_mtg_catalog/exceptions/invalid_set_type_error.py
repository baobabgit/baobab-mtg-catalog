"""Erreur de validation pour un type d'extension inconnu."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidSetTypeError(InvalidDomainValueError):
    """Levée lorsqu'une valeur de type de set n'est pas dans le référentiel."""
