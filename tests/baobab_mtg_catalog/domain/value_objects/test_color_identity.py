"""Tests pour ``ColorIdentity``."""

import pytest

from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.exceptions import InvalidColorIdentityError


class TestColorIdentity:
    """Construction, ordre WUBRG et sérialisation primitive."""

    def test_empty_identity(self) -> None:
        """Identité vide et factory ``empty``."""
        assert ColorIdentity.empty().is_empty()
        assert not list(ColorIdentity.empty())

    def test_from_iterable_dedupes_and_orders(self) -> None:
        """Doublons absorbés, ordre WUBRG sur itération."""
        ci = ColorIdentity.from_iterable([Color.RED, Color.BLUE, Color.RED])
        assert ci.ordered_colors() == (Color.BLUE, Color.RED)
        assert ci.to_primitive() == ["U", "R"]

    def test_invalid_element_type(self) -> None:
        """Seules les instances ``Color`` sont admises."""
        with pytest.raises(InvalidColorIdentityError):
            ColorIdentity.from_iterable([Color.RED, 0])  # type: ignore[list-item]
