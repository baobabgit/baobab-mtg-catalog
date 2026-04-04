"""Erreur de validation pour une entité ``CardPrinting`` incohérente."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardPrintingError(InvalidDomainValueError):
    """Levée lorsque les invariants d'un printing catalogue ne sont pas respectés."""
