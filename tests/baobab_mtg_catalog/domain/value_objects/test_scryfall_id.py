"""Tests pour ``ScryfallId``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions import InvalidScryfallIdError


class TestScryfallId:
    """UUID Scryfall normalisé."""

    def test_parse_normalizes_case(self) -> None:
        """UUID en minuscules canoniques."""
        raw = "550E8400-E29B-41D4-A716-446655440000"
        sid = ScryfallId.parse(raw)
        assert sid.value == "550e8400-e29b-41d4-a716-446655440000"

    @pytest.mark.parametrize("raw", ["", "not-a-uuid", "550e8400-e29b-41d4-a716"])
    def test_invalid(self, raw: str) -> None:
        """Entrées non UUID."""
        with pytest.raises(InvalidScryfallIdError):
            ScryfallId.parse(raw)
