"""Tests pour ``CollectorNumber``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.exceptions import InvalidCollectorNumberError


class TestCollectorNumber:
    """Numéros de collection alphanumériques."""

    def test_parse_preserves_zeros(self) -> None:
        """Les zéros non significatifs typographiques sont conservés."""
        assert CollectorNumber.parse("  001a ").value == "001a"

    def test_parse_star_glyph(self) -> None:
        """Glyphe étoile autorisé pour certaines promos."""
        cn = CollectorNumber.parse("★")
        assert cn.value == "★"

    @pytest.mark.parametrize("raw", ["", "   ", "12 34", "x" * 70])
    def test_parse_invalid(self, raw: str) -> None:
        """Vide, espaces internes, trop long."""
        with pytest.raises(InvalidCollectorNumberError):
            CollectorNumber.parse(raw)
