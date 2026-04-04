"""Tests pour ``uuid_canon``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions import InvalidOracleIdError


class TestUuidCanon:
    """Canonisation d'UUID partagée."""

    def test_valid(self) -> None:
        """UUID valide normalisé."""
        assert (
            canonize_uuid_string(
                " 550E8400-E29B-41D4-A716-446655440000 ",
                exc_cls=InvalidOracleIdError,
                invalid_message="x",
            )
            == "550e8400-e29b-41d4-a716-446655440000"
        )

    def test_invalid_raises(self) -> None:
        """UUID invalide propage l'exception demandée."""
        with pytest.raises(InvalidOracleIdError):
            canonize_uuid_string(
                "nope",
                exc_cls=InvalidOracleIdError,
                invalid_message="bad",
            )
