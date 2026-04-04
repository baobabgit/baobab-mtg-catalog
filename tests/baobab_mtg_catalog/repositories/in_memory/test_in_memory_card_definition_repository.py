"""Tests pour :class:`InMemoryCardDefinitionRepository`."""

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
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.exceptions import (
    CardDefinitionNotFoundError,
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_definition_repository import (
    InMemoryCardDefinitionRepository,
)


def _face() -> CardFace:
    return CardFace(
        name="Bear",
        normalized_name="bear",
        mana_cost=ManaCost.parse("{1}{G}"),
        type_line=CardTypeLine.parse("Creature — Bear"),
        oracle_text="",
        colors=frozenset({Color.GREEN}),
        power="2",
        toughness="2",
    )


def _definition(**overrides: Any) -> CardDefinition:
    f = _face()
    base: dict[str, Any] = {
        "card_definition_id": CardDefinitionIdentifier.parse(
            "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        ),
        "oracle_id": OracleId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        "name": f.name,
        "normalized_name": f.normalized_name,
        "mana_cost": f.mana_cost,
        "mana_value": 2.0,
        "type_line": f.type_line,
        "oracle_text": f.oracle_text,
        "colors": f.colors,
        "color_identity": ColorIdentity.from_iterable([Color.GREEN]),
        "faces": (f,),
        "power": f.power,
        "toughness": f.toughness,
    }
    base.update(overrides)
    return CardDefinition(**base)


class TestInMemoryCardDefinitionRepository:
    """Définitions Oracle en mémoire."""

    def test_upsert_get_by_id_and_oracle(self) -> None:
        """Lecture par id métier et oracle id."""
        repo = InMemoryCardDefinitionRepository()
        d = _definition()
        repo.upsert(d)
        assert repo.get_by_id(d.card_definition_id) == d
        assert repo.get_by_oracle_id(d.oracle_id) == d

    def test_not_found(self) -> None:
        """Absents."""
        repo = InMemoryCardDefinitionRepository()
        with pytest.raises(CardDefinitionNotFoundError):
            repo.get_by_id(CardDefinitionIdentifier.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))
        with pytest.raises(CardDefinitionNotFoundError):
            repo.get_by_oracle_id(OracleId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd"))

    def test_conflict_oracle_reused(self) -> None:
        """Deux ids métier distincts pour un même oracle."""
        repo = InMemoryCardDefinitionRepository()
        repo.upsert(_definition())
        other = _definition(
            card_definition_id=CardDefinitionIdentifier.parse(
                "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
            ),
        )
        with pytest.raises(RepositoryEntityConflictError):
            repo.upsert(other)

    def test_list_by_normalized_name(self) -> None:
        """Filtre simple sur le nom normalisé."""
        repo = InMemoryCardDefinitionRepository()
        f1 = CardFace(
            name="Shared Alpha",
            normalized_name="shared",
            mana_cost=ManaCost.parse("{1}{G}"),
            type_line=CardTypeLine.parse("Creature — Bear"),
            oracle_text="",
            colors=frozenset({Color.GREEN}),
            power="2",
            toughness="2",
        )
        f2 = CardFace(
            name="Shared Beta",
            normalized_name="shared",
            mana_cost=ManaCost.parse("{1}{G}"),
            type_line=CardTypeLine.parse("Creature — Bear"),
            oracle_text="",
            colors=frozenset({Color.GREEN}),
            power="2",
            toughness="2",
        )
        d1 = _definition(
            card_definition_id=CardDefinitionIdentifier.parse(
                "11111111-1111-4111-8111-111111111111"
            ),
            oracle_id=OracleId.parse("22222222-2222-4222-8222-222222222222"),
            name=f1.name,
            normalized_name=f1.normalized_name,
            faces=(f1,),
        )
        d2 = _definition(
            card_definition_id=CardDefinitionIdentifier.parse(
                "33333333-3333-4333-8333-333333333333"
            ),
            oracle_id=OracleId.parse("44444444-4444-4444-8444-444444444444"),
            name=f2.name,
            normalized_name=f2.normalized_name,
            faces=(f2,),
        )
        repo.upsert(d1)
        repo.upsert(d2)
        got = repo.list_by_normalized_name("shared")
        assert len(got) == 2
        assert got[0].card_definition_id.value < got[1].card_definition_id.value

    def test_list_all_sorted(self) -> None:
        """Ordre déterministe."""
        repo = InMemoryCardDefinitionRepository()
        repo.upsert(
            _definition(
                card_definition_id=CardDefinitionIdentifier.parse(
                    "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
                ),
                oracle_id=OracleId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
            )
        )
        repo.upsert(_definition())
        keys = [d.card_definition_id.value for d in repo.list_all()]
        assert keys == sorted(keys)

    def test_upsert_same_id_changes_oracle_reindexes(self) -> None:
        """Correction d'oracle sur le même id métier : réindexation."""
        repo = InMemoryCardDefinitionRepository()
        did = CardDefinitionIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
        o1 = OracleId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
        o2 = OracleId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
        repo.upsert(_definition(card_definition_id=did, oracle_id=o1))
        repo.upsert(_definition(card_definition_id=did, oracle_id=o2))
        assert repo.get_by_oracle_id(o2).oracle_id == o2
        with pytest.raises(CardDefinitionNotFoundError):
            repo.get_by_oracle_id(o1)
