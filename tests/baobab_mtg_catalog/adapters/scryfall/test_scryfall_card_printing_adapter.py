"""Tests pour :class:`ScryfallCardPrintingAdapter`."""

import pytest

from baobab_mtg_catalog.adapters.scryfall.scryfall_card_printing_adapter import (
    ScryfallCardPrintingAdapter,
)
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions import InvalidPayloadError, MappingError


def _printing_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "card",
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "name": "Éclair",
        "printed_name": "Éclair",
        "mana_cost": "{R}",
        "cmc": 1.0,
        "type_line": "Instant",
        "oracle_text": "Deal 3",
        "colors": ["R"],
        "color_identity": ["R"],
        "lang": "fr",
        "rarity": "common",
        "finishes": ["nonfoil", "foil"],
        "collector_number": "12",
        "artist": "Artist",
        "released_at": "2020-01-15",
        "image_uris": {
            "small": "https://cards.example.com/small.jpg",
            "png": "https://cards.example.com/card.png",
        },
        "multiverse_id": 42,
    }
    base.update(overrides)
    return base


class TestScryfallCardPrintingAdapter:
    """Printing depuis Scryfall."""

    def test_happy_path(self) -> None:
        """Impression FR avec finitions et images."""
        p = ScryfallCardPrintingAdapter.to_card_printing(
            _printing_payload(),
            card_printing_id=CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            card_definition_id=CardDefinitionIdentifier.parse(
                "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
            ),
            set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        )
        assert p.language == Language.FR
        assert p.rarity == Rarity.COMMON
        assert Finish.FOIL in p.finishes and Finish.NONFOIL in p.finishes
        assert p.image_uris is not None
        assert p.multiverse_id is not None and p.multiverse_id.value == 42
        nk = p.natural_key()
        assert isinstance(nk, ScryfallId)
        assert nk.value == "dddddddd-dddd-4ddd-8ddd-dddddddddddd"

    def test_lang_default_en(self) -> None:
        """Langue absente → ``en``."""
        payload = _printing_payload()
        del payload["lang"]
        p = ScryfallCardPrintingAdapter.to_card_printing(
            payload,
            card_printing_id=CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            card_definition_id=CardDefinitionIdentifier.parse(
                "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
            ),
            set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        )
        assert p.language == Language.EN

    def test_finishes_missing_defaults_nonfoil(self) -> None:
        """Liste absente → nonfoil."""
        payload = _printing_payload()
        del payload["finishes"]
        p = ScryfallCardPrintingAdapter.to_card_printing(
            payload,
            card_printing_id=CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            card_definition_id=CardDefinitionIdentifier.parse(
                "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
            ),
            set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        )
        assert p.finishes == frozenset({Finish.NONFOIL})

    def test_missing_collector_number(self) -> None:
        """collector_number obligatoire."""
        payload = _printing_payload()
        del payload["collector_number"]
        with pytest.raises(InvalidPayloadError):
            ScryfallCardPrintingAdapter.to_card_printing(
                payload,
                card_printing_id=CardPrintingIdentifier.parse(
                    "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
                ),
                card_definition_id=CardDefinitionIdentifier.parse(
                    "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
                ),
                set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
            )

    def test_invalid_rarity_mapping_error(self) -> None:
        """Rareté inconnue."""
        with pytest.raises(MappingError):
            ScryfallCardPrintingAdapter.to_card_printing(
                _printing_payload(rarity="not_a_rarity"),
                card_printing_id=CardPrintingIdentifier.parse(
                    "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
                ),
                card_definition_id=CardDefinitionIdentifier.parse(
                    "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
                ),
                set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
            )
