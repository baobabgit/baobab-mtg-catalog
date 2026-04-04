"""Tests pour ``PrintingImageUris``."""

import pytest

from baobab_mtg_catalog.domain.card_printings.printing_image_uris import PrintingImageUris
from baobab_mtg_catalog.exceptions import InvalidCardPrintingError


class TestPrintingImageUris:
    """URIs d'illustration."""

    def test_minimal_one_uri(self) -> None:
        """Au moins une URI valide."""
        uris = PrintingImageUris(
            normal="https://cards.scryfall.io/normal/front/x/y/uuid.jpg",
        )
        assert uris.normal is not None
        assert uris.small is None

    def test_all_none_rejected(self) -> None:
        """Agrégat vide interdit."""
        with pytest.raises(InvalidCardPrintingError):
            PrintingImageUris()

    def test_invalid_scheme(self) -> None:
        """Schéma non http(s)."""
        with pytest.raises(InvalidCardPrintingError):
            PrintingImageUris(normal="ftp://example.com/x.png")

    def test_strip_empty_fields(self) -> None:
        """Champs vides ignorés ; il reste une URI valide."""
        uris = PrintingImageUris(
            small="  ",
            png="https://example.com/card.png",
        )
        assert uris.small is None
        assert uris.png == "https://example.com/card.png"

    def test_uri_too_long(self) -> None:
        """URI dépassant la longueur maximale."""
        long_uri = "https://example.com/" + ("x" * 2100)
        with pytest.raises(InvalidCardPrintingError):
            PrintingImageUris(normal=long_uri)
