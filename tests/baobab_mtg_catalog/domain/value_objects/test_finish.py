"""Tests pour ``Finish``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.exceptions import InvalidFinishError


class TestFinish:
    """Finitions d'impression."""

    def test_parse_known(self) -> None:
        """Finitions reconnues."""
        assert Finish.parse("FOIL") is Finish.FOIL
        assert Finish.parse("etched") is Finish.ETCHED

    @pytest.mark.parametrize("raw", ["", "holo"])
    def test_parse_invalid(self, raw: str) -> None:
        """Finition inconnue."""
        with pytest.raises(InvalidFinishError):
            Finish.parse(raw)
