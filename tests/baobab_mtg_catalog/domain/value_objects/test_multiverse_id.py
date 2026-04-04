"""Tests pour ``MultiverseId``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.exceptions import InvalidMultiverseIdError


class TestMultiverseId:
    """Entier Gatherer strictement positif."""

    def test_parse_from_str_and_int(self) -> None:
        """Construction depuis str ou int."""
        assert MultiverseId.parse("42").value == 42
        assert MultiverseId.parse(1).value == 1

    @pytest.mark.parametrize("raw", [0, -1, "0", "abc", ""])
    def test_invalid(self, raw: str | int) -> None:
        """Valeurs non positives ou non numériques."""
        with pytest.raises(InvalidMultiverseIdError):
            MultiverseId.parse(raw)
