"""Erreur de validation pour une finition d'impression inconnue."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidFinishError(InvalidDomainValueError):
    """Levée lorsqu'une finition n'est pas reconnue dans le modèle catalogue."""
