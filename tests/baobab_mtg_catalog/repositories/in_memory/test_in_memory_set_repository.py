"""Tests pour :class:`InMemorySetRepository`."""

from datetime import date
from typing import Any

import pytest

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import (
    RepositoryEntityConflictError,
    SetNotFoundError,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_set_repository import (
    InMemorySetRepository,
)


def _set(**overrides: Any) -> Set:
    base: dict[str, Any] = {
        "set_id": SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        "code": SetCode.parse("TST"),
        "name": "Test",
        "release_date": date(2020, 1, 1),
        "set_type": SetType.EXPANSION,
    }
    base.update(overrides)
    return Set(**base)


class TestInMemorySetRepository:
    """Stockage set en mémoire."""

    def test_upsert_get_by_id_and_code(self) -> None:
        """Enregistrement et lecture par id / code."""
        repo = InMemorySetRepository()
        st = _set()
        assert repo.upsert(st) == st
        assert repo.get_by_id(st.set_id) == st
        assert repo.get_by_code(st.code) == st

    def test_get_by_scryfall_set_id(self) -> None:
        """Index Scryfall optionnel."""
        repo = InMemorySetRepository()
        scry = ScryfallId.parse("11111111-1111-4111-8111-111111111111")
        st = _set(scryfall_set_id=scry)
        repo.upsert(st)
        assert repo.get_by_scryfall_set_id(scry) == st

    def test_get_by_id_not_found(self) -> None:
        """Absent par id."""
        with pytest.raises(SetNotFoundError):
            InMemorySetRepository().get_by_id(SetId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))

    def test_get_by_code_not_found(self) -> None:
        """Absent par code."""
        with pytest.raises(SetNotFoundError):
            InMemorySetRepository().get_by_code(SetCode.parse("MIS"))

    def test_get_by_scryfall_not_found(self) -> None:
        """Sans index Scryfall."""
        repo = InMemorySetRepository()
        repo.upsert(_set())
        with pytest.raises(SetNotFoundError):
            repo.get_by_scryfall_set_id(ScryfallId.parse("22222222-2222-4222-8222-222222222222"))

    def test_conflict_same_code_different_set_id(self) -> None:
        """Unicité du code d'extension."""
        repo = InMemorySetRepository()
        repo.upsert(_set())
        other = _set(
            set_id=SetId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        )
        with pytest.raises(RepositoryEntityConflictError):
            repo.upsert(other)

    def test_conflict_scryfall_id_reuse(self) -> None:
        """Unicité de l'id Scryfall set."""
        scry = ScryfallId.parse("33333333-3333-4333-8333-333333333333")
        repo = InMemorySetRepository()
        repo.upsert(_set(scryfall_set_id=scry))
        dup = _set(
            set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
            code=SetCode.parse("OTH"),
            scryfall_set_id=scry,
        )
        with pytest.raises(RepositoryEntityConflictError):
            repo.upsert(dup)

    def test_idempotent_upsert(self) -> None:
        """Même ``SetId`` / code : remplacement."""
        repo = InMemorySetRepository()
        a = _set(name="A")
        b = _set(name="B")
        repo.upsert(a)
        repo.upsert(b)
        assert repo.get_by_id(a.set_id).name == "B"

    def test_list_all_sorted_by_id(self) -> None:
        """Ordre déterministe."""
        repo = InMemorySetRepository()
        s2 = _set(
            set_id=SetId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
            code=SetCode.parse("ZZZ"),
        )
        s1 = _set()
        repo.upsert(s2)
        repo.upsert(s1)
        ids = [s.set_id.value for s in repo.list_all()]
        assert ids == sorted(ids)

    def test_upsert_same_id_changes_code_reindexes(self) -> None:
        """Même ``SetId`` avec nouveau code : ancien index code retiré."""
        repo = InMemorySetRepository()
        sid = SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
        repo.upsert(_set(set_id=sid, code=SetCode.parse("AAA")))
        repo.upsert(_set(set_id=sid, code=SetCode.parse("BBB")))
        assert repo.get_by_code(SetCode.parse("BBB")).set_id == sid
        with pytest.raises(SetNotFoundError):
            repo.get_by_code(SetCode.parse("AAA"))

    def test_upsert_same_id_replaces_scryfall_index(self) -> None:
        """Mise à jour idempotente : remplacement de l'index Scryfall."""
        repo = InMemorySetRepository()
        sid = SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
        s1 = ScryfallId.parse("11111111-1111-4111-8111-111111111111")
        s2 = ScryfallId.parse("22222222-2222-4222-8222-222222222222")
        repo.upsert(_set(set_id=sid, scryfall_set_id=s1))
        repo.upsert(_set(set_id=sid, scryfall_set_id=s2))
        assert repo.get_by_scryfall_set_id(s2).set_id == sid
        with pytest.raises(SetNotFoundError):
            repo.get_by_scryfall_set_id(s1)
