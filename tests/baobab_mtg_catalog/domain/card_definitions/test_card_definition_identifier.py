"""Tests pour ``CardDefinitionIdentifier``."""

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.exceptions import InvalidCardDefinitionIdentifierError


class TestCardDefinitionIdentifier:
    """UUID métier des définitions de carte."""

    def test_parse(self) -> None:
        """Normalisation UUID."""
        cid = CardDefinitionIdentifier.parse(" 11111111-1111-4111-8111-111111111111 ")
        assert cid.value == "11111111-1111-4111-8111-111111111111"

    def test_invalid(self) -> None:
        """UUID invalide."""
        with pytest.raises(InvalidCardDefinitionIdentifierError):
            CardDefinitionIdentifier.parse("bad")
