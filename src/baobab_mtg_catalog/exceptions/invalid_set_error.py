"""Erreur de validation pour une entité ``Set`` incohérente."""

from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)


class InvalidSetError(InvalidDomainValueError):
    """Levée lorsque les invariants d'un set catalogue ne sont pas respectés."""
