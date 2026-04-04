"""Adaptateur Scryfall JSON → :class:`CardDefinition`."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from baobab_mtg_catalog.adapters.scryfall.scryfall_normalize import (
    color_symbols_from_list,
    keywords_frozenset,
    mana_value_from_card,
    optional_multiverse_id,
    optional_scryfall_id,
    run_mapping,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import optional_str, require_str
from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_definitions.card_face import CardFace
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.exceptions.invalid_payload_error import InvalidPayloadError


def _mana_cost_from_face_field(raw: object) -> ManaCost:
    if raw is None:
        return ManaCost.empty()
    if not isinstance(raw, str):
        raise InvalidPayloadError("mana_cost doit être une chaîne ou null.")
    stripped = raw.strip()
    if not stripped:
        return ManaCost.empty()
    return run_mapping("mana_cost", lambda: ManaCost.parse(stripped))


def _face_from_mapping(face: Mapping[str, Any]) -> CardFace:
    name = require_str(face, "name")
    normalized_name = name.lower()
    mana_cost = _mana_cost_from_face_field(face.get("mana_cost"))
    type_line_text = require_str(face, "type_line")
    oracle_text = optional_str(face, "oracle_text") or ""
    colors = color_symbols_from_list(face.get("colors"))
    power = optional_str(face, "power")
    toughness = optional_str(face, "toughness")
    loyalty = optional_str(face, "loyalty")
    return run_mapping(
        "CardFace",
        lambda: CardFace(
            name=name,
            normalized_name=normalized_name,
            mana_cost=mana_cost,
            type_line=CardTypeLine.parse(type_line_text),
            oracle_text=oracle_text,
            colors=colors,
            power=power,
            toughness=toughness,
            loyalty=loyalty,
        ),
    )


def _face_from_root(card: Mapping[str, Any]) -> CardFace:
    synthetic: dict[str, Any] = {
        "name": require_str(card, "name"),
        "mana_cost": card.get("mana_cost"),
        "type_line": require_str(card, "type_line"),
        "oracle_text": card.get("oracle_text"),
        "colors": card.get("colors"),
        "power": card.get("power"),
        "toughness": card.get("toughness"),
        "loyalty": card.get("loyalty"),
    }
    return _face_from_mapping(cast(Mapping[str, Any], synthetic))


def _faces_tuple(payload: Mapping[str, Any]) -> tuple[CardFace, ...]:
    faces_raw = payload.get("card_faces")
    if isinstance(faces_raw, list) and faces_raw:
        faces: list[CardFace] = []
        for item in faces_raw:
            if not isinstance(item, Mapping):
                raise InvalidPayloadError("Chaque entrée de card_faces doit être un objet.")
            faces.append(_face_from_mapping(cast(Mapping[str, Any], item)))
        return tuple(faces)
    return (_face_from_root(payload),)


def _aggregate_oracle_text(payload: Mapping[str, Any], faces: tuple[CardFace, ...]) -> str:
    if len(faces) > 1:
        parts = [f.oracle_text.strip() for f in faces]
        joined = " // ".join(p for p in parts if p)
        root = optional_str(payload, "oracle_text")
        if joined:
            return joined
        return root or ""
    root = optional_str(payload, "oracle_text")
    if root is not None:
        return root
    return faces[0].oracle_text


def _aggregate_type_line(payload: Mapping[str, Any], faces: tuple[CardFace, ...]) -> str:
    root_tl = optional_str(payload, "type_line")
    if root_tl:
        return root_tl
    if len(faces) > 1:
        return " // ".join(f.type_line.value for f in faces)
    return faces[0].type_line.value


def _aggregate_colors(payload: Mapping[str, Any], faces: tuple[CardFace, ...]) -> frozenset[Color]:
    agg = color_symbols_from_list(payload.get("colors"))
    if agg:
        return agg
    if len(faces) > 1:
        merged: set[Color] = set()
        for face in faces:
            merged.update(face.colors)
        return frozenset(merged)
    return faces[0].colors


def _color_identity_from_payload(
    payload: Mapping[str, Any], fallback_colors: frozenset[Color]
) -> ColorIdentity:
    raw_ci = payload.get("color_identity")
    if isinstance(raw_ci, list) and raw_ci:
        colors = color_symbols_from_list(raw_ci)
        if colors:
            return ColorIdentity.from_iterable(colors)
    return ColorIdentity.from_iterable(fallback_colors)


class ScryfallCardDefinitionAdapter:
    """Transforme un objet ``card`` Scryfall en :class:`CardDefinition`."""

    @staticmethod
    def to_card_definition(  # pylint: disable=too-many-locals
        payload: Mapping[str, Any],
        *,
        card_definition_id: CardDefinitionIdentifier,
    ) -> CardDefinition:
        """Construit une définition Oracle depuis un payload carte Scryfall.

        :param payload: Objet carte JSON (champs ``oracle_*``, ``card_faces``, etc.).
        :param card_definition_id: Identifiant métier attribué par le référentiel.
        :returns: Carte logique normalisée.
        :raises InvalidPayloadError: Si la structure minimale est absente.
        :raises NormalizationError: Si une valeur est incohérente.
        :raises MappingError: Si le domaine rejette le résultat.
        """
        faces = _faces_tuple(payload)
        name = require_str(payload, "name")
        normalized_name = name.lower()
        oracle_text = _aggregate_oracle_text(payload, faces)
        type_line_str = _aggregate_type_line(payload, faces)
        agg_colors = _aggregate_colors(payload, faces)
        color_identity = _color_identity_from_payload(payload, agg_colors)
        mana_value = mana_value_from_card(payload)
        mana_cost = faces[0].mana_cost
        keywords = keywords_frozenset(payload.get("keywords"))
        oracle_id = run_mapping(
            "oracle_id", lambda: OracleId.parse(require_str(payload, "oracle_id"))
        )
        scryfall_card_id = optional_scryfall_id(payload, "id")
        multiverse_id = optional_multiverse_id(payload)
        if len(faces) > 1:
            power = None
            toughness = None
            loyalty = None
        else:
            power = faces[0].power
            toughness = faces[0].toughness
            loyalty = faces[0].loyalty
        type_line_vo = run_mapping("type_line", lambda: CardTypeLine.parse(type_line_str))
        return run_mapping(
            "CardDefinition",
            lambda: CardDefinition(
                card_definition_id=card_definition_id,
                oracle_id=oracle_id,
                name=name,
                normalized_name=normalized_name,
                mana_cost=mana_cost,
                mana_value=mana_value,
                type_line=type_line_vo,
                oracle_text=oracle_text,
                colors=agg_colors,
                color_identity=color_identity,
                faces=faces,
                keywords=keywords,
                power=power,
                toughness=toughness,
                loyalty=loyalty,
                scryfall_card_id=scryfall_card_id,
                multiverse_id=multiverse_id,
            ),
        )
