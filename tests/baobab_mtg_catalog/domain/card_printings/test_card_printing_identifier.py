"""Tests pour ``CardPrintingIdentifier``."""

import pytest

from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.exceptions import InvalidCardPrintingIdentifierError


class TestCardPrintingIdentifier:
    """UUID métier des printings."""

    def test_parse(self) -> None:
        """Normalisation UUID."""
        pid = CardPrintingIdentifier.parse(" 11111111-1111-4111-8111-111111111111 ")
        assert pid.value == "11111111-1111-4111-8111-111111111111"

    def test_invalid(self) -> None:
        """UUID invalide."""
        with pytest.raises(InvalidCardPrintingIdentifierError):
            CardPrintingIdentifier.parse("bad")
