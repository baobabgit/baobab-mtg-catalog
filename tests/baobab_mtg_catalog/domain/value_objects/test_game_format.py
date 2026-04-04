"""Tests pour ``GameFormat``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.game_format import GameFormat
from baobab_mtg_catalog.exceptions import InvalidGameFormatError


class TestGameFormat:
    """Slugs de format construit."""

    def test_parse_normalizes(self) -> None:
        """Minuscules et trim."""
        fmt = GameFormat.parse(" Standard ")
        assert fmt.value == "standard"

    @pytest.mark.parametrize("raw", ["", "A", "9fmt", "x" * 60])
    def test_invalid_slug(self, raw: str) -> None:
        """Slug hors contrainte."""
        with pytest.raises(InvalidGameFormatError):
            GameFormat.parse(raw)
