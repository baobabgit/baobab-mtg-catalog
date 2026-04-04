"""Tests pour ``Color``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.exceptions import InvalidColorError


class TestColor:
    """Scénarios de parsing et représentation des couleurs WUBRG."""

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("w", Color.WHITE),
            ("W", Color.WHITE),
            ("white", Color.WHITE),
            ("u", Color.BLUE),
            ("blue", Color.BLUE),
            ("b", Color.BLACK),
            ("r", Color.RED),
            ("g", Color.GREEN),
        ],
    )
    def test_parse_accepts_aliases(self, raw: str, expected: Color) -> None:
        """Les alias usuels sont acceptés."""
        assert Color.parse(raw) is expected

    @pytest.mark.parametrize("raw", ["", "  ", "X", "orange", "WW"])
    def test_parse_rejects_invalid(self, raw: str) -> None:
        """Les entrées hors WUBRG échouent."""
        with pytest.raises(InvalidColorError):
            Color.parse(raw)
