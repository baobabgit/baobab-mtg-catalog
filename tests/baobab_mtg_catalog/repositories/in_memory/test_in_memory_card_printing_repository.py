"""Tests pour :class:`InMemoryCardPrintingRepository`."""

from typing import Any

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions import (
    CardPrintingNotFoundError,
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_printing_repository import (
    InMemoryCardPrintingRepository,
)


def _printing(**overrides: Any) -> CardPrinting:
    base: dict[str, Any] = {
        "card_printing_id": CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        "card_definition_id": CardDefinitionIdentifier.parse(
            "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
        ),
        "set_id": SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        "collector_number": CollectorNumber.parse("1"),
        "language": Language.EN,
        "rarity": Rarity.COMMON,
        "finishes": frozenset({Finish.NONFOIL}),
        "scryfall_printing_id": ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd"),
    }
    base.update(overrides)
    return CardPrinting(**base)


class TestInMemoryCardPrintingRepository:
    """Printings en mémoire."""

    def test_upsert_get_by_id_natural_scryfall(self) -> None:
        """Clé naturelle Scryfall."""
        repo = InMemoryCardPrintingRepository()
        p = _printing()
        repo.upsert(p)
        assert repo.get_by_id(p.card_printing_id) == p
        assert repo.get_by_natural_key(p.natural_key()) == p
        assert (
            repo.get_by_scryfall_printing_id(
                ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
            )
            == p
        )

    def test_tuple_natural_key_without_scryfall(self) -> None:
        """Repli ``(set_id, collector, langue)``."""
        repo = InMemoryCardPrintingRepository()
        p = _printing(scryfall_printing_id=None)
        repo.upsert(p)
        assert repo.get_by_natural_key(p.natural_key()) == p
        with pytest.raises(CardPrintingNotFoundError):
            repo.get_by_scryfall_printing_id(
                ScryfallId.parse("11111111-1111-4111-8111-111111111111")
            )

    def test_list_by_set_and_collector(self) -> None:
        """Filtres simples."""
        repo = InMemoryCardPrintingRepository()
        sid = SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
        p1 = _printing(
            card_printing_id=CardPrintingIdentifier.parse("11111111-1111-4111-8111-111111111111"),
            scryfall_printing_id=ScryfallId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        )
        p2 = _printing(
            card_printing_id=CardPrintingIdentifier.parse("22222222-2222-4222-8222-222222222222"),
            collector_number=CollectorNumber.parse("2"),
            scryfall_printing_id=ScryfallId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        )
        p3 = _printing(
            card_printing_id=CardPrintingIdentifier.parse("33333333-3333-4333-8333-333333333333"),
            collector_number=CollectorNumber.parse("1a"),
            language=Language.FR,
            scryfall_printing_id=ScryfallId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        )
        repo.upsert(p1)
        repo.upsert(p2)
        repo.upsert(p3)
        by_set = repo.list_by_set_id(sid)
        assert len(by_set) == 3
        cn1 = repo.list_by_set_and_collector(sid, CollectorNumber.parse("1"))
        assert cn1 == (p1,)

    def test_conflict_natural_key(self) -> None:
        """Collision de clé naturelle."""
        repo = InMemoryCardPrintingRepository()
        sid = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        repo.upsert(_printing())
        other = _printing(
            card_printing_id=CardPrintingIdentifier.parse("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"),
            scryfall_printing_id=sid,
        )
        with pytest.raises(RepositoryEntityConflictError):
            repo.upsert(other)

    def test_not_found(self) -> None:
        """Absents."""
        repo = InMemoryCardPrintingRepository()
        with pytest.raises(CardPrintingNotFoundError):
            repo.get_by_id(CardPrintingIdentifier.parse("ffffffff-ffff-4fff-8fff-ffffffffffff"))

    def test_upsert_same_id_changes_scryfall_reindexes(self) -> None:
        """Même ``CardPrintingIdentifier`` avec nouveau Scryfall : index mis à jour."""
        repo = InMemoryCardPrintingRepository()
        pid = CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
        s1 = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        s2 = ScryfallId.parse("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee")
        repo.upsert(_printing(card_printing_id=pid, scryfall_printing_id=s1))
        repo.upsert(_printing(card_printing_id=pid, scryfall_printing_id=s2))
        assert repo.get_by_scryfall_printing_id(s2).card_printing_id == pid
        with pytest.raises(CardPrintingNotFoundError):
            repo.get_by_scryfall_printing_id(s1)

    def test_get_by_natural_key_tuple_not_found(self) -> None:
        """Clé locale inexistante."""
        repo = InMemoryCardPrintingRepository()
        repo.upsert(_printing(scryfall_printing_id=None))
        bad_key = (
            SetId.parse("ffffffff-ffff-4fff-8fff-ffffffffffff"),
            CollectorNumber.parse("99"),
            Language.JA,
        )
        with pytest.raises(CardPrintingNotFoundError):
            repo.get_by_natural_key(bad_key)
