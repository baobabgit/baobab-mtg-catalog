"""Tests pour :class:`ScryfallCardDefinitionAdapter`."""

import pytest

from baobab_mtg_catalog.adapters.scryfall.scryfall_card_definition_adapter import (
    ScryfallCardDefinitionAdapter,
)
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.exceptions import InvalidPayloadError, MappingError


def _cid() -> CardDefinitionIdentifier:
    return CardDefinitionIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")


def _mono_card(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "card",
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
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
    }
    base.update(overrides)
    return base


class TestScryfallCardDefinitionAdapter:
    """Carte logique depuis Scryfall."""

    def test_mono_face_happy_path(self) -> None:
        """Carte simple."""
        card = ScryfallCardDefinitionAdapter.to_card_definition(
            _mono_card(), card_definition_id=_cid()
        )
        assert not card.is_multi_faced()
        assert card.oracle_id.value == "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
        assert card.mana_cost == ManaCost.parse("{R}")
        assert card.colors == frozenset({Color.RED})
        assert "instant" in card.keywords
        assert card.scryfall_card_id is not None

    def test_missing_oracle_id(self) -> None:
        """oracle_id obligatoire."""
        with pytest.raises(InvalidPayloadError):
            ScryfallCardDefinitionAdapter.to_card_definition(
                _mono_card(oracle_id=None),
                card_definition_id=_cid(),
            )

    def test_invalid_oracle_uuid_mapping_error(self) -> None:
        """UUID oracle invalide → :class:`MappingError`."""
        with pytest.raises(MappingError):
            ScryfallCardDefinitionAdapter.to_card_definition(
                _mono_card(oracle_id="bad"),
                card_definition_id=_cid(),
            )

    def test_multi_face_mdfc(self) -> None:
        """MDFC : agrégats et P/T carte absents."""
        payload = _mono_card(
            name="Daybound // Nightbound",
            mana_cost="",
            cmc=0.0,
            colors=[],
            color_identity=["G"],
            type_line="Enchantment // Enchantment",
            oracle_text="",
            card_faces=[
                {
                    "name": "Daybound",
                    "mana_cost": "{1}{G}",
                    "type_line": "Enchantment",
                    "oracle_text": "Day stuff",
                    "colors": ["G"],
                },
                {
                    "name": "Nightbound",
                    "mana_cost": "",
                    "type_line": "Enchantment",
                    "oracle_text": "Night stuff",
                    "colors": [],
                },
            ],
        )
        del payload["mana_cost"]
        card = ScryfallCardDefinitionAdapter.to_card_definition(payload, card_definition_id=_cid())
        assert card.is_multi_faced()
        assert card.power is None and card.toughness is None
        assert card.oracle_text == "Day stuff // Night stuff"
        assert card.mana_cost == ManaCost.parse("{1}{G}")

    def test_card_faces_non_object(self) -> None:
        """Entrée card_faces invalide."""
        with pytest.raises(InvalidPayloadError):
            ScryfallCardDefinitionAdapter.to_card_definition(
                _mono_card(card_faces=[1, 2, 3]),
                card_definition_id=_cid(),
            )
