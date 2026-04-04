"""Payloads JSON Scryfall minimaux partagés par les tests services."""

from __future__ import annotations


def set_payload_lea(**overrides: object) -> dict[str, object]:
    """Objet set Scryfall type *Limited Edition Alpha*."""
    base: dict[str, object] = {
        "object": "set",
        "id": "11111111-1111-4111-8111-111111111111",
        "code": "lea",
        "name": "Limited Edition Alpha",
        "set_type": "core",
        "released_at": "1993-08-05",
        "digital": False,
        "foil_only": False,
    }
    base.update(overrides)
    return base


def mono_card_lightning_lea(**overrides: object) -> dict[str, object]:
    """Carte *Lightning Bolt* dans LEA."""
    base: dict[str, object] = {
        "object": "card",
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "multiverse_id": 600,
        "name": "Lightning Bolt",
        "mana_cost": "{R}",
        "cmc": 1.0,
        "type_line": "Instant",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "colors": ["R"],
        "color_identity": ["R"],
        "keywords": ["Instant"],
        "lang": "en",
        "rarity": "common",
        "finishes": ["nonfoil"],
        "collector_number": "116",
        "artist": "Christopher Rush",
        "set": "lea",
    }
    base.update(overrides)
    return base


def bear_card_lea(**overrides: object) -> dict[str, object]:
    """Carte *Grizzly Bears* dans LEA."""
    base: dict[str, object] = {
        "object": "card",
        "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "oracle_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "multiverse_id": 601,
        "name": "Grizzly Bears",
        "mana_cost": "{1}{G}",
        "cmc": 2.0,
        "type_line": "Creature — Bear",
        "oracle_text": "",
        "colors": ["G"],
        "color_identity": ["G"],
        "lang": "en",
        "rarity": "common",
        "finishes": ["nonfoil"],
        "collector_number": "5",
        "set": "lea",
    }
    base.update(overrides)
    return base
