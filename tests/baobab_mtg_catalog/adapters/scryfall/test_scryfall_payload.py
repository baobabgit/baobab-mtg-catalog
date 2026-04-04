"""Tests pour ``scryfall_payload``."""

import pytest

from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import (
    optional_str,
    require_str,
)
from baobab_mtg_catalog.exceptions import InvalidPayloadError


class TestScryfallPayload:
    """Accès typé aux champs JSON."""

    def test_require_str_ok(self) -> None:
        """Chaîne valide."""
        assert require_str({"k": " x "}, "k") == "x"

    def test_require_str_missing(self) -> None:
        """Champ absent."""
        with pytest.raises(InvalidPayloadError):
            require_str({}, "k")

    def test_optional_str_none(self) -> None:
        """Absent ou null."""
        assert optional_str({}, "k") is None
        assert optional_str({"k": None}, "k") is None

    def test_optional_str_bad_type(self) -> None:
        """Type incorrect."""
        with pytest.raises(InvalidPayloadError):
            optional_str({"k": 1}, "k")
