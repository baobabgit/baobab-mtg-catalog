"""Adaptateur Scryfall JSON → :class:`~baobab_mtg_catalog.domain.sets.set.Set`."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from baobab_mtg_catalog.adapters.scryfall.scryfall_normalize import (
    optional_scryfall_id,
    optional_set_code,
    parse_iso_date_required,
    resolve_set_type,
    run_mapping,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import require_str
from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions.invalid_payload_error import InvalidPayloadError


class ScryfallSetAdapter:
    """Transforme un objet ``set`` Scryfall en entité :class:`Set` du domaine.

    Les identifiants métier (``SetId``) sont fournis par l'appelant pour rester
    alignés sur la persistance et l'import idempotent (résolution préalable par
    :meth:`Set.natural_key`).
    """

    @staticmethod
    def to_set(  # pylint: disable=too-many-locals
        payload: Mapping[str, Any], *, set_id: SetId
    ) -> Set:
        """Construit un :class:`Set` depuis un payload JSON Scryfall.

        :param payload: Objet set tel que renvoyé par l'API Scryfall.
        :param set_id: Identifiant métier à attribuer dans le référentiel.
        :returns: Extension normalisée.
        :raises InvalidPayloadError: Si la structure minimale est absente.
        :raises NormalizationError: Si une valeur est incohérente.
        :raises MappingError: Si le domaine rejette les données mappées.
        """
        code_str = require_str(payload, "code")
        name = require_str(payload, "name")
        set_type_raw = require_str(payload, "set_type")
        set_type = resolve_set_type(set_type_raw)
        released_raw = require_str(payload, "released_at")
        release_date = parse_iso_date_required(released_raw, field="released_at")
        code = run_mapping("code", lambda: SetCode.parse(code_str))
        card_count = ScryfallSetAdapter._optional_non_negative_int(payload, "card_count")
        digital = payload.get("digital")
        foil_only = payload.get("foil_only")
        digital_only = bool(digital) if isinstance(digital, bool) else False
        foil_only_b = bool(foil_only) if isinstance(foil_only, bool) else False
        scryfall_set_id = optional_scryfall_id(payload, "id")
        parent = optional_set_code(payload, "parent_set_code")
        block = optional_set_code(payload, "block_code")
        return run_mapping(
            "Set",
            lambda: Set(
                set_id=set_id,
                code=code,
                name=name,
                release_date=release_date,
                set_type=set_type,
                card_count=card_count,
                digital_only=digital_only,
                foil_only=foil_only_b,
                scryfall_set_id=scryfall_set_id,
                parent_set_code=parent,
                block_code=block,
            ),
        )

    @staticmethod
    def _optional_non_negative_int(container: Mapping[str, Any], key: str) -> int | None:
        value = container.get(key)
        if value is None:
            return None
        if not isinstance(value, int):
            raise InvalidPayloadError(f"Champ {key!r} doit être un entier ou null.")
        if value < 0:
            raise InvalidPayloadError(f"Champ {key!r} ne peut pas être négatif.")
        return value
