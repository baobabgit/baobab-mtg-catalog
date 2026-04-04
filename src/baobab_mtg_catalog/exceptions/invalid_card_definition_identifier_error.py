"""Erreur de validation pour un identifiant métier de définition de carte."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardDefinitionIdentifierError(InvalidDomainValueError):
    """Levée lorsqu'un ``CardDefinitionIdentifier`` est absent ou mal formé."""
