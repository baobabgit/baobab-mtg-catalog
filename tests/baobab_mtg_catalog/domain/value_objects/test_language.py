"""Tests pour ``Language``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.exceptions import InvalidLanguageError


class TestLanguage:
    """Parsing des codes langue supportés."""

    def test_parse_known(self) -> None:
        """Codes ISO / Scryfall usuels."""
        assert Language.parse("  FR ") is Language.FR
        assert Language.parse("zhs") is Language.ZHS

    @pytest.mark.parametrize("raw", ["", "xx", "EN_US"])
    def test_parse_unknown(self, raw: str) -> None:
        """Codes inconnus rejetés."""
        with pytest.raises(InvalidLanguageError):
            Language.parse(raw)
