"""Tests pour ``CardFace``."""

from typing import Any, cast

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_face import CardFace
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.exceptions import InvalidCardFaceError


class TestCardFace:
    """Validation d'une face."""

    def test_minimal_creature(self) -> None:
        """Face créature avec P/T."""
        face = CardFace(
            name="Grizzly Bears",
            normalized_name="grizzly bears",
            mana_cost=ManaCost.parse("{1}{G}"),
            type_line=CardTypeLine.parse("Creature — Bear"),
            oracle_text="",
            colors=frozenset({Color.GREEN}),
            power="2",
            toughness="2",
        )
        assert face.power == "2"
        assert face.oracle_text == ""

    def test_invalid_power_character(self) -> None:
        """Caractère interdit en force."""
        with pytest.raises(InvalidCardFaceError):
            CardFace(
                name="X",
                normalized_name="x",
                mana_cost=ManaCost.empty(),
                type_line=CardTypeLine.parse("Creature — Test"),
                oracle_text="",
                colors=frozenset(),
                power="2@",
                toughness="2",
            )

    def test_invalid_color_element(self) -> None:
        """Élément non ``Color`` dans l'ensemble."""
        with pytest.raises(InvalidCardFaceError):
            CardFace(
                name="X",
                normalized_name="x",
                mana_cost=ManaCost.empty(),
                type_line=CardTypeLine.parse("Artifact"),
                oracle_text="",
                colors=frozenset({Color.RED, cast(Any, object())}),
            )
