"""Validation de champs pour les impressions catalogue."""

from __future__ import annotations

from urllib.parse import urlparse

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)

_MAX_URI_LEN: int = 2048


def validate_optional_http_uri(
    raw: str | None,
    *,
    label: str,
    exc_cls: type[BaobabMtgCatalogException],
) -> str | None:
    """Valide une URI HTTP(S) optionnelle (strip, schéma, longueur).

    :param raw: URI brute ou ``None``.
    :param label: Libellé pour les messages d'erreur.
    :param exc_cls: Exception projet à lever.
    :returns: URI stripée ou ``None`` si absente / vide après strip.
    """
    if raw is None:
        return None
    text = raw.strip()
    if not text:
        return None
    if len(text) > _MAX_URI_LEN:
        raise exc_cls(f"{label} dépasse {_MAX_URI_LEN} caractères: {raw!r}.")
    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise exc_cls(f"{label} doit être une URI http(s) avec hôte: {raw!r}.")
    return text
