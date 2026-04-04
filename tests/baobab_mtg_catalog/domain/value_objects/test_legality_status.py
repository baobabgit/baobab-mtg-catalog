"""Tests pour ``LegalityStatus``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.legality_status import LegalityStatus
from baobab_mtg_catalog.exceptions import InvalidLegalityStatusError


class TestLegalityStatus:
    """Statuts de légalité."""

    def test_parse_known(self) -> None:
        """Valeurs snake_case usuelles."""
        assert LegalityStatus.parse("NOT_LEGAL") is LegalityStatus.NOT_LEGAL
        assert LegalityStatus.parse("banned") is LegalityStatus.BANNED

    @pytest.mark.parametrize("raw", ["", "maybe"])
    def test_invalid(self, raw: str) -> None:
        """Statut inconnu."""
        with pytest.raises(InvalidLegalityStatusError):
            LegalityStatus.parse(raw)
