"""Tests pour l'entité ``Set``."""

from datetime import date
from typing import Any

import pytest

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import InvalidDomainValueError, InvalidSetError


def _sample_set_id_a() -> SetId:
    return SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")


def _sample_set_id_b() -> SetId:
    return SetId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")


def _valid_set(**overrides: Any) -> Set:
    params: dict[str, Any] = {
        "set_id": _sample_set_id_a(),
        "code": SetCode.parse("TST"),
        "name": "Test Set",
        "release_date": date(2020, 1, 17),
        "set_type": SetType.EXPANSION,
    }
    params.update(overrides)
    return Set(**params)


class TestSet:
    """Invariants, identité et clé naturelle."""

    def test_invalid_set_error_chain(self) -> None:
        """Les erreurs set restent dans la hiérarchie domaine."""
        assert issubclass(InvalidSetError, InvalidDomainValueError)

    def test_name_trimmed(self) -> None:
        """Le nom est normalisé (strip)."""
        s = _valid_set(name="  Phyrexia  ")
        assert s.name == "Phyrexia"

    def test_optional_fields(self) -> None:
        """Métadonnées optionnelles et drapeaux."""
        scry = ScryfallId.parse("11111111-1111-4111-8111-111111111111")
        parent = SetCode.parse("MOM")
        block = SetCode.parse("SOM")
        s = _valid_set(
            card_count=280,
            digital_only=True,
            foil_only=False,
            scryfall_set_id=scry,
            parent_set_code=parent,
            block_code=block,
        )
        assert s.card_count == 280
        assert s.digital_only is True
        assert s.scryfall_set_id == scry
        assert s.parent_set_code == parent
        assert s.block_code == block

    def test_equality_by_set_id_only(self) -> None:
        """Égalité sur ``SetId`` uniquement (même code, ids différents)."""
        a = _valid_set(set_id=_sample_set_id_a(), code=SetCode.parse("ONE"))
        b = _valid_set(set_id=_sample_set_id_b(), code=SetCode.parse("ONE"))
        assert a != b
        assert a.same_extension_as(b)

    def test_same_id_equal_and_hashable(self) -> None:
        """Même ``SetId`` => égalité ; utilisable en clé de dict."""
        sid = _sample_set_id_a()
        x = _valid_set(set_id=sid, name="A")
        y = _valid_set(set_id=sid, name="B")
        assert x == y
        assert hash(x) == hash(y)
        assert {x: 1}[y] == 1

    def test_set_not_equal_to_non_set(self) -> None:
        """Un set n'est pas égal à une valeur d'un autre type."""
        assert _valid_set() != "nope"

    def test_natural_key_is_code(self) -> None:
        """Clé d'idempotence d'import = code extension."""
        s = _valid_set(code=SetCode.parse("mh3"))
        assert s.natural_key().value == "MH3"

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"name": ""},
            {"name": "   "},
            {"name": "x" * 501},
            {"card_count": -1},
            {"release_date": date(1990, 1, 1)},
            {"release_date": date(2150, 1, 1)},
        ],
    )
    def test_invalid_invariants(self, kwargs: dict[str, object]) -> None:
        """Violations des invariants métier."""
        with pytest.raises(InvalidSetError):
            _valid_set(**kwargs)

    def test_name_control_char_rejected(self) -> None:
        """Caractères de contrôle interdits dans le nom."""
        with pytest.raises(InvalidSetError):
            _valid_set(name="bad\x01name")
