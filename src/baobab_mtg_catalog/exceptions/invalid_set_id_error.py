"""Erreur de validation pour un identifiant métier de set invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidSetIdError(InvalidDomainValueError):
    """Levée lorsqu'un ``SetId`` (UUID métier) est absent ou mal formé."""
