"""Erreur de validation pour un identifiant de format de jeu."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidGameFormatError(InvalidDomainValueError):
    """Levée lorsqu'un slug de format (standard, modern, …) est mal formé."""
