"""Tests pour ``CardDefinition``."""

import math
from typing import Any

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_definitions.card_face import CardFace
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions import (
    InvalidCardDefinitionError,
    InvalidDomainValueError,
)


def _cid() -> CardDefinitionIdentifier:
    return CardDefinitionIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")


def _oid() -> OracleId:
    return OracleId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")


def _mono_face() -> CardFace:
    return CardFace(
        name="Elvish Mystic",
        normalized_name="elvish mystic",
        mana_cost=ManaCost.parse("{G}"),
        type_line=CardTypeLine.parse("Creature — Elf Druid"),
        oracle_text="{T}: Add {G}.",
        colors=frozenset({Color.GREEN}),
        power="1",
        toughness="1",
    )


def _card(**overrides: Any) -> CardDefinition:
    face = _mono_face()
    params: dict[str, Any] = {
        "card_definition_id": _cid(),
        "oracle_id": _oid(),
        "name": face.name,
        "normalized_name": face.normalized_name,
        "mana_cost": face.mana_cost,
        "mana_value": 1.0,
        "type_line": face.type_line,
        "oracle_text": face.oracle_text,
        "colors": face.colors,
        "color_identity": ColorIdentity.from_iterable([Color.GREEN]),
        "faces": (face,),
        "keywords": frozenset(),
        "power": face.power,
        "toughness": face.toughness,
        "loyalty": face.loyalty,
    }
    params.update(overrides)
    return CardDefinition(**params)


class TestCardDefinition:
    """Carte logique mono / multi-face et identité."""

    def test_invalid_error_chain(self) -> None:
        """Hiérarchie d'exceptions."""
        assert issubclass(InvalidCardDefinitionError, InvalidDomainValueError)

    def test_mono_face_happy_path(self) -> None:
        """Carte simple avec options."""
        scry = ScryfallId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
        mv = MultiverseId.parse(123_456)
        card = _card(
            scryfall_card_id=scry,
            multiverse_id=mv,
            keywords=frozenset({"Flying", "FIRST STRIKE"}),
        )
        assert card.keywords == frozenset({"flying", "first strike"})
        assert card.scryfall_card_id == scry
        assert card.multiverse_id == mv
        assert not card.is_multi_faced()
        assert card.primary_face.name == "Elvish Mystic"

    def test_multi_face(self) -> None:
        """MDFC : P/T au niveau carte interdits."""
        front = CardFace(
            name="Front Face",
            normalized_name="front face",
            mana_cost=ManaCost.parse("{2}{U}"),
            type_line=CardTypeLine.parse("Creature — Illusion"),
            oracle_text="Flying",
            colors=frozenset({Color.BLUE}),
            power="3",
            toughness="3",
        )
        back = CardFace(
            name="Back Face",
            normalized_name="back face",
            mana_cost=ManaCost.empty(),
            type_line=CardTypeLine.parse("Enchantment"),
            oracle_text="",
            colors=frozenset(),
        )
        card = CardDefinition(
            card_definition_id=_cid(),
            oracle_id=_oid(),
            name="Front Face // Back Face",
            normalized_name="front face // back face",
            mana_cost=front.mana_cost,
            mana_value=3.0,
            type_line=CardTypeLine.parse("Creature — Illusion // Enchantment"),
            oracle_text="Flying //",
            colors=frozenset({Color.BLUE}),
            color_identity=ColorIdentity.from_iterable([Color.BLUE]),
            faces=(front, back),
        )
        assert card.is_multi_faced()
        assert card.primary_face.power == "3"
        assert card.power is None

    def test_equality_by_definition_id(self) -> None:
        """Égalité sur identifiant métier uniquement."""
        a = _card()
        b = _card(
            card_definition_id=CardDefinitionIdentifier.parse(
                "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
            ),
        )
        assert a != b
        assert a.same_logical_card_as(b)

    def test_natural_key_is_oracle_id(self) -> None:
        """Clé d'idempotence = oracle id."""
        card = _card()
        assert card.natural_key() == _oid()

    def test_empty_faces_rejected(self) -> None:
        """Au moins une face obligatoire."""
        with pytest.raises(InvalidCardDefinitionError):
            _card(faces=())

    def test_mana_cost_must_match_first_face(self) -> None:
        """Cohérence du coût avec la face initiale."""
        face = _mono_face()
        with pytest.raises(InvalidCardDefinitionError):
            CardDefinition(
                card_definition_id=_cid(),
                oracle_id=_oid(),
                name=face.name,
                normalized_name=face.normalized_name,
                mana_cost=ManaCost.parse("{2}"),
                mana_value=1.0,
                type_line=face.type_line,
                oracle_text=face.oracle_text,
                colors=face.colors,
                color_identity=ColorIdentity.from_iterable([Color.GREEN]),
                faces=(face,),
            )

    def test_mono_mismatch_rejected(self) -> None:
        """Mono-face : champs carte / face alignés."""
        face = _mono_face()
        with pytest.raises(InvalidCardDefinitionError):
            CardDefinition(
                card_definition_id=_cid(),
                oracle_id=_oid(),
                name="Wrong Name",
                normalized_name=face.normalized_name,
                mana_cost=face.mana_cost,
                mana_value=1.0,
                type_line=face.type_line,
                oracle_text=face.oracle_text,
                colors=face.colors,
                color_identity=ColorIdentity.from_iterable([Color.GREEN]),
                faces=(face,),
            )

    def test_multi_face_with_card_level_pt_rejected(self) -> None:
        """Multi-face sans P/T carte."""
        front = CardFace(
            name="A",
            normalized_name="a",
            mana_cost=ManaCost.parse("{R}"),
            type_line=CardTypeLine.parse("Creature — Goblin"),
            oracle_text="",
            colors=frozenset({Color.RED}),
            power="1",
            toughness="1",
        )
        back = CardFace(
            name="B",
            normalized_name="b",
            mana_cost=ManaCost.empty(),
            type_line=CardTypeLine.parse("Sorcery"),
            oracle_text="Burn",
            colors=frozenset({Color.RED}),
        )
        with pytest.raises(InvalidCardDefinitionError):
            CardDefinition(
                card_definition_id=_cid(),
                oracle_id=_oid(),
                name="A // B",
                normalized_name="a // b",
                mana_cost=front.mana_cost,
                mana_value=1.0,
                type_line=CardTypeLine.parse("Creature — Goblin // Sorcery"),
                oracle_text=" // Burn",
                colors=frozenset({Color.RED}),
                color_identity=ColorIdentity.from_iterable([Color.RED]),
                faces=(front, back),
                power="1",
            )

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"mana_value": -1.0},
            {"mana_value": math.nan},
        ],
    )
    def test_invalid_mana_value(self, kwargs: dict[str, Any]) -> None:
        """Valeur de mana invalide."""
        with pytest.raises(InvalidCardDefinitionError):
            _card(**kwargs)

    def test_empty_keyword_rejected(self) -> None:
        """Mot-clé vide dans l'ensemble."""
        with pytest.raises(InvalidCardDefinitionError):
            _card(keywords=frozenset({"  "}))
