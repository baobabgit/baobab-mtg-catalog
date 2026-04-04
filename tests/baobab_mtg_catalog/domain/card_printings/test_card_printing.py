"""Tests pour ``CardPrinting``."""

from datetime import date
from typing import Any, cast

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.printing_image_uris import PrintingImageUris
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions import InvalidCardPrintingError, InvalidDomainValueError


def _printing(**overrides: Any) -> CardPrinting:
    base: dict[str, Any] = {
        "card_printing_id": CardPrintingIdentifier.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        "card_definition_id": CardDefinitionIdentifier.parse(
            "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
        ),
        "set_id": SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
        "collector_number": CollectorNumber.parse("123"),
        "language": Language.EN,
        "rarity": Rarity.RARE,
        "finishes": frozenset({Finish.NONFOIL, Finish.FOIL}),
    }
    base.update(overrides)
    return CardPrinting(**base)


class TestCardPrinting:
    """Impression catalogue."""

    def test_invalid_error_chain(self) -> None:
        """Hiérarchie d'exceptions."""
        assert issubclass(InvalidCardPrintingError, InvalidDomainValueError)

    def test_happy_path_with_optional_fields(self) -> None:
        """Champs optionnels et natural key Scryfall."""
        scry = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        mv = MultiverseId.parse(99_999)
        imgs = PrintingImageUris(small="https://example.com/s.jpg")
        p = _printing(
            scryfall_printing_id=scry,
            multiverse_id=mv,
            artist="  Alice Artist  ",
            image_uris=imgs,
            released_at=date(2020, 1, 15),
        )
        assert p.artist == "Alice Artist"
        assert p.natural_key() == scry
        assert p.image_uris == imgs
        assert p.multiverse_id == mv

    def test_natural_key_fallback_without_scryfall(self) -> None:
        """Repli sur triplet set / collector / langue."""
        p = _printing(scryfall_printing_id=None)
        assert p.natural_key() == (
            p.set_id,
            p.collector_number,
            p.language,
        )

    def test_equality_by_printing_id(self) -> None:
        """Égalité sur identifiant métier."""
        a = _printing()
        b = _printing(
            card_printing_id=CardPrintingIdentifier.parse("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"),
            collector_number=CollectorNumber.parse("999"),
        )
        assert a != b
        assert a.same_catalog_printing_as(b) is False

    def test_same_catalog_printing_as_scryfall(self) -> None:
        """Même clé naturelle Scryfall malgré UUID métier différent."""
        sid = ScryfallId.parse("ffffffff-ffff-4fff-8fff-ffffffffffff")
        a = _printing(
            card_printing_id=CardPrintingIdentifier.parse("11111111-1111-4111-8111-111111111111"),
            scryfall_printing_id=sid,
        )
        b = _printing(
            card_printing_id=CardPrintingIdentifier.parse("22222222-2222-4222-8222-222222222222"),
            scryfall_printing_id=sid,
        )
        assert a != b
        assert a.same_catalog_printing_as(b)

    def test_empty_finishes_rejected(self) -> None:
        """Au moins une finition."""
        with pytest.raises(InvalidCardPrintingError):
            _printing(finishes=frozenset())

    def test_invalid_finish_element(self) -> None:
        """Élément non ``Finish`` dans l'ensemble."""
        with pytest.raises(InvalidCardPrintingError):
            _printing(
                finishes=frozenset({Finish.NONFOIL, cast(Any, object())}),
            )

    def test_artist_whitespace_becomes_none(self) -> None:
        """Artiste vide après strip."""
        p = _printing(artist="   ")
        assert p.artist is None

    def test_artist_too_long(self) -> None:
        """Nom d'artiste trop long."""
        with pytest.raises(InvalidCardPrintingError):
            _printing(artist="x" * 501)

    def test_released_at_out_of_range(self) -> None:
        """Date de sortie invraisemblable."""
        with pytest.raises(InvalidCardPrintingError):
            _printing(released_at=date(1800, 1, 1))

    def test_str_enum_finish_dedup(self) -> None:
        """``StrEnum`` : chaîne égale à une valeur ne duplique pas le set."""
        p = _printing(finishes=frozenset({Finish.FOIL, cast(Any, "foil")}))
        assert len(p.finishes) == 1

    def test_eq_notimplemented_and_hash(self) -> None:
        """Comparaison avec un non-printing et hachage stable."""
        p = _printing()
        assert p.__eq__(object()) is NotImplemented
        assert isinstance(hash(p), int)
