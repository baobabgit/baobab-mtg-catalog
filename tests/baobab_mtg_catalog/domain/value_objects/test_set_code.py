"""Tests pour ``SetCode``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import InvalidSetCodeError


class TestSetCode:
    """Normalisation et validation des codes d'extension."""

    def test_parse_uppercases(self) -> None:
        """Casse normalisée en majuscules."""
        code = SetCode.parse(" one ")
        assert code.value == "ONE"

    @pytest.mark.parametrize("raw", ["", "TOOLONGCODE9", "ab_c", "space here"])
    def test_parse_invalid(self, raw: str) -> None:
        """Longueur et alphabet contrôlés."""
        with pytest.raises(InvalidSetCodeError):
            SetCode.parse(raw)
