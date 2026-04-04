"""Normalisation et mapping contrôlé Scryfall → types du domaine."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from datetime import date
from typing import Any, TypeVar

from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import optional_mapping
from baobab_mtg_catalog.domain.card_printings.printing_image_uris import PrintingImageUris
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)
from baobab_mtg_catalog.exceptions.invalid_finish_error import InvalidFinishError
from baobab_mtg_catalog.exceptions.invalid_payload_error import InvalidPayloadError
from baobab_mtg_catalog.exceptions.mapping_error import MappingError
from baobab_mtg_catalog.exceptions.normalization_error import NormalizationError

_T = TypeVar("_T")

_SCRYFALL_SET_TYPE_CANON: dict[str, str] = {
    "masters": "expansion",
    "future": "expansion",
    "planechase_deck": "planechase",
}

_SCRYFALL_LANGUAGE_ALIASES: dict[str, str] = {
    "ph": "phyrexian",
}

_RARITY_ALIASES: dict[str, str] = {
    "timeshifted": "special",
}


def run_mapping(description: str, func: Callable[[], _T]) -> _T:
    """Exécute un appel domaine et encapsule les erreurs en :class:`MappingError`.

    Les erreurs de structure (:class:`InvalidPayloadError`) et de normalisation
    (:class:`NormalizationError`) sont propagées telles quelles pour garder une
    distinction nette avec les échecs de construction domaine.

    :param description: Contexte humain (ex. nom du champ).
    :param func: Fabrique d'objet valeur ou entité.
    :returns: Résultat de ``func``.
    :raises InvalidPayloadError: Erreur de forme du JSON (non enveloppée).
    :raises NormalizationError: Valeur Scryfall incohérente (non enveloppée).
    :raises MappingError: Autre :class:`BaobabMtgCatalogException` du domaine.
    """
    try:
        return func()
    except InvalidPayloadError:
        raise
    except NormalizationError:
        raise
    except BaobabMtgCatalogException as exc:
        raise MappingError(f"{description}: {exc}") from exc


def resolve_set_type(raw: str) -> SetType:
    """Mappe un ``set_type`` Scryfall vers :class:`SetType`.

    :param raw: Valeur brute Scryfall.
    :returns: Type normalisé domaine.
    :raises NormalizationError: Si la valeur est vide.
    :raises MappingError: Si aucune correspondance n'existe.
    """
    key = raw.strip().lower()
    if not key:
        raise NormalizationError("Le type de set Scryfall est vide.")
    canon = _SCRYFALL_SET_TYPE_CANON.get(key, key)
    return run_mapping("set_type", lambda: SetType.parse(canon))


def language_from_scryfall(code: str) -> Language:
    """Interprète le code langue Scryfall (avec alias connus).

    :param code: Champ ``lang`` carte.
    :returns: Langue domaine.
    :raises InvalidPayloadError: Si vide.
    :raises MappingError: Si code inconnu.
    """
    trimmed = code.strip().lower()
    if not trimmed:
        raise InvalidPayloadError("Le code de langue Scryfall est vide.")
    mapped = _SCRYFALL_LANGUAGE_ALIASES.get(trimmed, trimmed)
    return run_mapping("langue", lambda: Language.parse(mapped))


def rarity_from_scryfall(raw: str) -> Rarity:
    """Mappe une rareté Scryfall (avec alias).

    :param raw: Champ ``rarity``.
    :returns: Rareté domaine.
    :raises MappingError: Si valeur inconnue.
    """
    key = raw.strip().lower()
    canon = _RARITY_ALIASES.get(key, key)
    return run_mapping("rareté", lambda: Rarity.parse(canon))


def finishes_from_scryfall(raw: object) -> frozenset[Finish]:
    """Construit l'ensemble des finitions à partir de la liste Scryfall.

    Les finitions inconnues du domaine sont ignorées. Si la liste est vide ou
    n'apporte aucune finition reconnue, :attr:`Finish.NONFOIL` est ajouté.

    :param raw: Liste ``finishes`` ou ``None``.
    :returns: Ensemble non vide de :class:`Finish`.
    :raises InvalidPayloadError: Si le type n'est pas une liste lorsque présent.
    """
    if raw is None:
        return frozenset({Finish.NONFOIL})
    if not isinstance(raw, list):
        raise InvalidPayloadError("Le champ finishes doit être une liste JSON.")
    parsed: set[Finish] = set()
    for item in raw:
        if not isinstance(item, str):
            continue
        try:
            parsed.add(Finish.parse(item))
        except InvalidFinishError:
            continue
    if not parsed:
        parsed.add(Finish.NONFOIL)
    return frozenset(parsed)


def parse_iso_date_required(raw: str, *, field: str) -> date:
    """Parse une date ISO ``YYYY-MM-DD`` obligatoire.

    :param raw: Chaîne Scryfall.
    :param field: Nom du champ pour le message d'erreur.
    :returns: Date Python.
    :raises NormalizationError: Si format invalide.
    """
    text = raw.strip()
    if not text:
        raise NormalizationError(f"Date vide pour {field}.")
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise NormalizationError(f"Date invalide pour {field}: {raw!r}.") from exc


def parse_iso_date_optional(raw: object, *, field: str) -> date | None:
    """Parse une date ISO optionnelle.

    :param raw: Chaîne, ``null`` ou absent représenté par ``None`` en amont.
    :param field: Nom du champ pour le message d'erreur.
    :returns: Date ou ``None``.
    :raises NormalizationError: Si présent mais mal formé.
    """
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise NormalizationError(f"Date {field} doit être une chaîne ou null.")
    stripped = raw.strip()
    if not stripped:
        return None
    try:
        return date.fromisoformat(stripped)
    except ValueError as exc:
        raise NormalizationError(f"Date invalide pour {field}: {raw!r}.") from exc


def mana_value_from_card(payload: Mapping[str, Any]) -> float:
    """Lit la valeur de mana convertie (``mana_value`` prioritaire, sinon ``cmc``).

    :param payload: Objet carte Scryfall.
    :returns: CMC non négatif.
    :raises InvalidPayloadError: Si aucune valeur exploitable.
    :raises NormalizationError: Si la valeur n'est pas numérique valide.
    """
    if "mana_value" in payload and payload["mana_value"] is not None:
        token = payload["mana_value"]
    elif "cmc" in payload and payload["cmc"] is not None:
        token = payload["cmc"]
    else:
        raise InvalidPayloadError("Champ mana_value ou cmc obligatoire pour la carte.")
    if isinstance(token, bool):
        raise NormalizationError("La valeur de mana ne peut pas être booléenne.")
    try:
        value = float(token)
    except (TypeError, ValueError) as exc:
        raise NormalizationError(f"Valeur de mana non numérique: {token!r}.") from exc
    if value < 0 or math.isnan(value):
        raise NormalizationError(f"Valeur de mana invalide: {value!r}.")
    return value


def _color_from_json_symbol(symbol: str) -> Color:
    """Parse un symbole WUBRG Scryfall en :class:`Color` avec enveloppe :class:`MappingError`."""
    return run_mapping("couleur", lambda: Color.parse(symbol))


def color_symbols_from_list(raw: object) -> frozenset[Color]:
    """Interprète une liste de symboles WUBRG Scryfall.

    :param raw: Liste ou ``None`` (traité comme vide).
    :returns: Couleurs domaine.
    :raises InvalidPayloadError: Si type incorrect.
    """
    if raw is None:
        return frozenset()
    if not isinstance(raw, list):
        raise InvalidPayloadError("colors / color_identity doit être une liste JSON.")
    colors_out: list[Color] = []
    for item in raw:
        if not isinstance(item, str):
            raise InvalidPayloadError("Symbole de couleur attendu sous forme de chaîne.")
        colors_out.append(_color_from_json_symbol(item))
    return frozenset(colors_out)


def optional_scryfall_id(container: Mapping[str, Any], key: str) -> ScryfallId | None:
    """Construit un :class:`ScryfallId` optionnel depuis un champ UUID.

    :param container: Objet JSON.
    :param key: Nom du champ (ex. ``id``).
    :returns: Identifiant ou ``None`` si absent / null / vide.
    """
    text = container.get(key)
    if text is None:
        return None
    if not isinstance(text, str):
        raise InvalidPayloadError(f"Champ {key!r} doit être une chaîne UUID ou null.")
    stripped = text.strip()
    if not stripped:
        return None
    return run_mapping(key, lambda: ScryfallId.parse(stripped))


def optional_multiverse_id(payload: Mapping[str, Any]) -> MultiverseId | None:
    """Extrait le premier multiverse id positif disponible.

    :param payload: Objet carte Scryfall.
    :returns: Identifiant ou ``None``.
    """
    mid = payload.get("multiverse_id")
    if isinstance(mid, int) and mid >= 1:
        return MultiverseId(mid)
    mids = payload.get("multiverse_ids")
    if isinstance(mids, list):
        for item in mids:
            if isinstance(item, int) and item >= 1:
                return MultiverseId(item)
    return None


def optional_set_code(container: Mapping[str, Any], key: str) -> SetCode | None:
    """Parse un code set optionnel.

    :param container: Objet JSON.
    :param key: Champ code (ex. ``parent_set_code``).
    :returns: Code domaine ou ``None``.
    """
    text = container.get(key)
    if text is None:
        return None
    if not isinstance(text, str):
        raise InvalidPayloadError(f"Champ {key!r} doit être une chaîne ou null.")
    stripped = text.strip()
    if not stripped:
        return None
    return run_mapping(key, lambda: SetCode.parse(stripped))


def image_uris_from_scryfall(payload: Mapping[str, Any]) -> PrintingImageUris | None:
    """Construit :class:`PrintingImageUris` depuis ``image_uris`` Scryfall.

    :param payload: Objet carte.
    :returns: ``PrintingImageUris`` ou ``None`` si aucune URI exploitable.
    :raises MappingError: Si les URIs sont syntaxiquement rejetées par le domaine.
    """
    raw = optional_mapping(payload, "image_uris")
    if raw is None:
        return None
    kwargs: dict[str, str] = {}
    for key in ("small", "normal", "large", "png", "art_crop", "border_crop"):
        val = raw.get(key)
        if isinstance(val, str):
            stripped = val.strip()
            if stripped:
                kwargs[key] = stripped
    if not kwargs:
        return None
    return run_mapping("image_uris", lambda: PrintingImageUris(**kwargs))


def keywords_frozenset(raw: object) -> frozenset[str]:
    """Normalise la liste ``keywords`` Scryfall.

    :param raw: Liste ou ``None``.
    :returns: Ensemble de chaînes brutes (normalisation fines via le domaine).
    :raises InvalidPayloadError: Si type invalide ou élément non chaîne.
    """
    if raw is None:
        return frozenset()
    if not isinstance(raw, list):
        raise InvalidPayloadError("keywords doit être une liste JSON.")
    result: list[str] = []
    for item in raw:
        if not isinstance(item, str):
            raise InvalidPayloadError("Chaque mot-clé doit être une chaîne.")
        result.append(item)
    return frozenset(result)
