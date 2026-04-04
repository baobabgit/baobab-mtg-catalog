"""Canonisation d'UUID pour les identifiants externes du catalogue."""

from __future__ import annotations

import uuid
from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


def canonize_uuid_string(
    raw: str,
    *,
    exc_cls: type[BaobabMtgCatalogException],
    invalid_message: str,
) -> str:
    """Normalise une entrée UUID ou lève ``exc_cls`` avec ``invalid_message``.

    :param raw: Chaîne brute candidate.
    :type raw: str
    :param exc_cls: Exception projet à lever en cas d'échec (message unique).
    :type exc_cls: type[BaobabMtgCatalogException]
    :param invalid_message: Message d'erreur déjà formaté si besoin.
    :type invalid_message: str
    :returns: UUID canonique en minuscules avec tirets.
    :rtype: str
    """
    candidate = raw.strip().lower()
    try:
        return str(uuid.UUID(candidate))
    except ValueError as exc:
        raise exc_cls(invalid_message) from exc
