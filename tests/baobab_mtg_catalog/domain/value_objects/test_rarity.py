"""Tests pour ``Rarity``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.exceptions import InvalidRarityError


class TestRarity:
    """Valeurs de rareté catalogue."""

    def test_parse_common_variants(self) -> None:
        """Raretés standard."""
        assert Rarity.parse("mythic") is Rarity.MYTHIC
        assert Rarity.parse("COMMON") is Rarity.COMMON

    @pytest.mark.parametrize("raw", ["", "ultra_rare"])
    def test_parse_invalid(self, raw: str) -> None:
        """Valeurs hors référentiel."""
        with pytest.raises(InvalidRarityError):
            Rarity.parse(raw)
