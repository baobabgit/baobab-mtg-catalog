"""Tests pour :class:`ScryfallSetAdapter`."""

import pytest

from baobab_mtg_catalog.adapters.scryfall.scryfall_set_adapter import ScryfallSetAdapter
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import InvalidPayloadError, MappingError


def _set_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "set",
        "id": "11111111-1111-4111-8111-111111111111",
        "code": "lea",
        "name": "Limited Edition Alpha",
        "set_type": "core",
        "released_at": "1993-08-05",
        "digital": False,
        "foil_only": False,
    }
    base.update(overrides)
    return base


class TestScryfallSetAdapter:
    """Adaptateur set Scryfall."""

    def test_happy_path(self) -> None:
        """Set nominal."""
        st = ScryfallSetAdapter.to_set(
            _set_payload(),
            set_id=SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        )
        assert st.natural_key() == SetCode.parse("lea")
        assert st.scryfall_set_id is not None
        assert st.scryfall_set_id.value == "11111111-1111-4111-8111-111111111111"

    def test_missing_released_at(self) -> None:
        """Date obligatoire."""
        with pytest.raises(InvalidPayloadError):
            ScryfallSetAdapter.to_set(
                _set_payload(released_at=None),
                set_id=SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            )

    def test_unknown_set_type(self) -> None:
        """Type non mappable."""
        with pytest.raises(MappingError):
            ScryfallSetAdapter.to_set(
                _set_payload(set_type="not_a_real_type_ever"),
                set_id=SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            )

    def test_card_count_negative(self) -> None:
        """card_count négatif rejeté."""
        with pytest.raises(InvalidPayloadError):
            ScryfallSetAdapter.to_set(
                _set_payload(card_count=-1),
                set_id=SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            )
