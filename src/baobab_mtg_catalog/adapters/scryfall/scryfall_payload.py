"""Lecture typée des champs d'un payload JSON Scryfall (``Mapping``)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from baobab_mtg_catalog.exceptions.invalid_payload_error import InvalidPayloadError


def require_str(container: Mapping[str, Any], key: str) -> str:
    """Exige une chaîne non vide après strip.

    :param container: Objet JSON (carte, set, face, etc.).
    :param key: Nom du champ.
    :returns: Texte stripé non vide.
    :raises InvalidPayloadError: Si absent, mauvais type ou vide.
    """
    value = container.get(key)
    if value is None:
        raise InvalidPayloadError(f"Champ obligatoire manquant: {key!r}.")
    if not isinstance(value, str):
        raise InvalidPayloadError(f"Champ {key!r} doit être une chaîne.")
    text = value.strip()
    if not text:
        raise InvalidPayloadError(f"Champ {key!r} ne peut pas être vide.")
    return text


def optional_str(container: Mapping[str, Any], key: str) -> str | None:
    """Lit une chaîne optionnelle (``null`` ou absente autorisés).

    :param container: Objet JSON source.
    :param key: Nom du champ.
    :returns: Texte stripé ou ``None`` si absent / null / vide après strip.
    :raises InvalidPayloadError: Si le type n'est pas chaîne ni null absent.
    """
    value = container.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidPayloadError(f"Champ {key!r} doit être une chaîne ou null.")
    stripped = value.strip()
    return stripped if stripped else None


def require_mapping(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    """Exige un sous-objet JSON.

    :param container: Parent JSON.
    :param key: Nom du champ objet.
    :returns: Sous-mapping.
    :raises InvalidPayloadError: Si absent ou non objet.
    """
    value = container.get(key)
    if value is None:
        raise InvalidPayloadError(f"Objet obligatoire manquant: {key!r}.")
    if not isinstance(value, Mapping):
        raise InvalidPayloadError(f"Champ {key!r} doit être un objet JSON.")
    return cast(Mapping[str, Any], value)


def optional_mapping(container: Mapping[str, Any], key: str) -> Mapping[str, Any] | None:
    """Lit un sous-objet optionnel.

    :param container: Parent JSON.
    :param key: Nom du champ.
    :returns: Sous-mapping ou ``None``.
    :raises InvalidPayloadError: Si présent mais non objet.
    """
    value = container.get(key)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise InvalidPayloadError(f"Champ {key!r} doit être un objet JSON ou null.")
    return cast(Mapping[str, Any], value)


def require_list(container: Mapping[str, Any], key: str) -> list[Any]:
    """Exige une liste JSON (éventuellement vide).

    :param container: Parent JSON.
    :param key: Nom du champ.
    :returns: Liste brute.
    :raises InvalidPayloadError: Si absent ou non liste.
    """
    value = container.get(key)
    if value is None:
        raise InvalidPayloadError(f"Liste obligatoire manquante: {key!r}.")
    if not isinstance(value, list):
        raise InvalidPayloadError(f"Champ {key!r} doit être une liste JSON.")
    return value


def optional_list(container: Mapping[str, Any], key: str) -> list[Any] | None:
    """Lit une liste optionnelle.

    :param container: Parent JSON.
    :param key: Nom du champ.
    :returns: Liste ou ``None``.
    :raises InvalidPayloadError: Si présent mais non liste.
    """
    value = container.get(key)
    if value is None:
        return None
    if not isinstance(value, list):
        raise InvalidPayloadError(f"Champ {key!r} doit être une liste JSON ou null.")
    return value
