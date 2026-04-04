"""Erreur de validation pour un code de langue non pris en charge."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidLanguageError(InvalidDomainValueError):
    """Levée lorsqu'un code de langue ne correspond pas au référentiel métier."""
