"""Tests pour ``OracleId``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.exceptions import InvalidOracleIdError


class TestOracleId:
    """UUID oracle id."""

    def test_parse_valid(self) -> None:
        """UUID valide accepté."""
        oid = OracleId.parse("6b3b3c5f-97f2-4e0b-9c1d-8e2f3a4b5c6d")
        assert oid.value == "6b3b3c5f-97f2-4e0b-9c1d-8e2f3a4b5c6d"

    def test_invalid(self) -> None:
        """UUID invalide rejeté."""
        with pytest.raises(InvalidOracleIdError):
            OracleId.parse("zzz")
