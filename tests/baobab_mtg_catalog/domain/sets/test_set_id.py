"""Tests pour ``SetId``."""

import pytest

from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.exceptions import InvalidSetIdError


class TestSetId:
    """Identifiant métier UUID du set."""

    def test_parse_normalizes(self) -> None:
        """Casse et espaces normalisés."""
        sid = SetId.parse(" 123E4567-E89B-12D3-A456-426614174000 ")
        assert sid.value == "123e4567-e89b-12d3-a456-426614174000"

    def test_invalid_uuid(self) -> None:
        """Valeur non UUID rejetée."""
        with pytest.raises(InvalidSetIdError):
            SetId.parse("not-uuid")

    def test_to_primitive(self) -> None:
        """Sérialisation primitive."""
        sid = SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
        assert sid.to_primitive() == "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
