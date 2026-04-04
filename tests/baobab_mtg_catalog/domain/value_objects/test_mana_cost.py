"""Tests pour ``ManaCost``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.exceptions import InvalidManaCostError


class TestManaCost:
    """Syntaxe des symboles de coût de mana."""

    def test_empty(self) -> None:
        """Coût vide autorisé."""
        assert ManaCost.empty().is_empty()
        assert ManaCost.parse("   ").value == ""

    def test_valid_sequences(self) -> None:
        """Concaténation de symboles."""
        cost = ManaCost.parse("{2}{W/U}{X}")
        assert cost.value == "{2}{W/U}{X}"

    @pytest.mark.parametrize("raw", ["{W", "W}", "{W}{}", "x" * 300])
    def test_invalid_syntax(self, raw: str) -> None:
        """Accolades mal formées ou chaîne trop longue."""
        with pytest.raises(InvalidManaCostError):
            ManaCost.parse(raw)
