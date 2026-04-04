"""Tests pour ``SetType``."""

import pytest

from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.exceptions import InvalidSetTypeError


class TestSetType:
    """Types d'extension catalogue."""

    def test_parse_known(self) -> None:
        """Valeurs snake_case reconnues."""
        assert SetType.parse("EXPANSION") is SetType.EXPANSION
        assert SetType.parse(" draft_innovation ") is SetType.DRAFT_INNOVATION

    @pytest.mark.parametrize("raw", ["", "unknown_type"])
    def test_parse_invalid(self, raw: str) -> None:
        """Vide ou inconnu."""
        with pytest.raises(InvalidSetTypeError):
            SetType.parse(raw)
