"""Fonctions de validation de texte partagées pour les définitions de carte."""

from __future__ import annotations

import re

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)

_CONTROL_CHARS: re.Pattern[str] = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_MAX_PT_LEN: int = 24
_PT_LOYALTY_PATTERN: re.Pattern[str] = re.compile(
    r"^[\d½∞*+/?\-Ww,\s]+$",
    re.UNICODE,
)


def validate_text_field(
    raw: str,
    *,
    label: str,
    max_len: int,
    allow_empty: bool,
    exc_cls: type[BaobabMtgCatalogException],
) -> str:
    """Valide et normalise une chaîne métier (strip, longueur, contrôle).

    :param raw: Texte brut.
    :param label: Libellé humain pour les messages d'erreur.
    :param max_len: Longueur maximale après strip.
    :param allow_empty: Si faux, une chaîne vide après strip est rejetée.
    :param exc_cls: Exception projet à lever.
    :returns: Texte stripé.
    """
    text = raw.strip()
    if not allow_empty and not text:
        raise exc_cls(f"{label} ne peut pas être vide.")
    if len(text) > max_len:
        raise exc_cls(f"{label} dépasse {max_len} caractères: {raw!r}.")
    if _CONTROL_CHARS.search(text):
        raise exc_cls(f"{label} contient des caractères de contrôle.")
    return text


def validate_optional_pt_loyalty(
    value: str | None,
    *,
    label: str,
    exc_cls: type[BaobabMtgCatalogException],
) -> str | None:
    """Valide force, endurance ou loyauté affichée (symboles Oracle usuels).

    :param value: Valeur brute ou ``None``.
    :param label: Libellé pour le message d'erreur.
    :param exc_cls: Exception projet à lever.
    :returns: Valeur stripée ou ``None`` si absent / vide.
    """
    if value is None:
        return None
    token = value.strip()
    if not token:
        return None
    if len(token) > _MAX_PT_LEN:
        raise exc_cls(f"{label} dépasse {_MAX_PT_LEN} caractères: {value!r}.")
    if not _PT_LOYALTY_PATTERN.fullmatch(token):
        raise exc_cls(f"{label} a un format non reconnu: {value!r}.")
    return token
