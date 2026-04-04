"""Erreur de validation pour une face de carte logique."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardFaceError(InvalidDomainValueError):
    """Levée lorsque les invariants d'une :class:`CardFace` ne sont pas respectés."""
