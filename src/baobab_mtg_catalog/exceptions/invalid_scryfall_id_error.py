"""Erreur de validation pour un identifiant Scryfall (carte / printing)."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidScryfallIdError(InvalidDomainValueError):
    """Levée lorsqu'un UUID Scryfall attendu est absent ou mal formé."""
