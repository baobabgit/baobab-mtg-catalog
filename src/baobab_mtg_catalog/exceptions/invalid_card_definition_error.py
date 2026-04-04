"""Erreur de validation pour une entité ``CardDefinition`` incohérente."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidCardDefinitionError(InvalidDomainValueError):
    """Levée lorsque les invariants d'une carte logique ne sont pas respectés."""
