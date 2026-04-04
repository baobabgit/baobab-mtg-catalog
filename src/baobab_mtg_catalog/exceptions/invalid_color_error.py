"""Erreur de validation pour une couleur de mana invalide."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidColorError(InvalidDomainValueError):
    """Levée lorsqu'un symbole ou littéral de couleur n'est pas reconnu."""
