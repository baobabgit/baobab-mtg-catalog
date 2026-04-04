"""Tests pour ``CardTypeLine``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.exceptions import InvalidCardTypeLineError


class TestCardTypeLine:
    """Ligne de types Oracle."""

    def test_parse_trims(self) -> None:
        """Espaces de tête / fin ignorés."""
        line = CardTypeLine.parse("  Creature — Human  ")
        assert line.value == "Creature — Human"

    @pytest.mark.parametrize("raw", ["", "  ", "\x01broken"])
    def test_invalid(self, raw: str) -> None:
        """Vide ou caractères de contrôle."""
        with pytest.raises(InvalidCardTypeLineError):
            CardTypeLine.parse(raw)
