"""Tests pour ``scryfall_normalize``."""

import pytest

from baobab_mtg_catalog.adapters.scryfall.scryfall_normalize import (
    finishes_from_scryfall,
    language_from_scryfall,
    mana_value_from_card,
    rarity_from_scryfall,
    resolve_set_type,
    run_mapping,
)
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.exceptions import (
    InvalidDomainValueError,
    InvalidPayloadError,
    MappingError,
    NormalizationError,
)


class TestScryfallNormalize:
    """Normalisation Scryfall."""

    def test_run_mapping_wraps_domain_error(self) -> None:
        """Erreur domaine → :class:`MappingError`."""
        with pytest.raises(MappingError) as ctx:

            def _boom() -> None:
                raise InvalidDomainValueError("boom")

            run_mapping("étape", _boom)
        assert isinstance(ctx.value.__cause__, InvalidDomainValueError)

    def test_resolve_set_type_masters_alias(self) -> None:
        """Alias ``masters`` → expansion."""
        assert resolve_set_type("masters") == SetType.EXPANSION

    def test_resolve_set_type_empty(self) -> None:
        """Type vide."""
        with pytest.raises(NormalizationError):
            resolve_set_type("   ")

    def test_language_ph_alias(self) -> None:
        """Alias ``ph`` → phyrexian."""
        assert language_from_scryfall("ph") == Language.PHYREXIAN

    def test_rarity_timeshifted_alias(self) -> None:
        """Alias ``timeshifted`` → special."""
        assert rarity_from_scryfall("timeshifted") == Rarity.SPECIAL

    def test_finishes_unknown_defaults_nonfoil(self) -> None:
        """Finitions inconnues ignorées ; défaut nonfoil."""
        got = finishes_from_scryfall(["galaxy_foil", "unknown"])
        assert got == frozenset({Finish.NONFOIL})

    def test_finishes_none_defaults(self) -> None:
        """``None`` → nonfoil."""
        assert finishes_from_scryfall(None) == frozenset({Finish.NONFOIL})

    def test_finishes_bad_type(self) -> None:
        """Type non liste."""
        with pytest.raises(InvalidPayloadError):
            finishes_from_scryfall("foil")

    def test_mana_value_prefers_mana_value(self) -> None:
        """Priorité ``mana_value`` sur ``cmc``."""
        payload = {"mana_value": 2.0, "cmc": 9.0}
        assert mana_value_from_card(payload) == 2.0

    def test_mana_value_missing(self) -> None:
        """Absence totale."""
        with pytest.raises(InvalidPayloadError):
            mana_value_from_card({})

    def test_mana_value_negative(self) -> None:
        """CMC négatif."""
        with pytest.raises(NormalizationError):
            mana_value_from_card({"cmc": -1.0})
