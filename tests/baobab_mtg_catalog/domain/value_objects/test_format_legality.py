"""Tests pour ``FormatLegality``."""

from baobab_mtg_catalog.domain.value_objects.format_legality import FormatLegality
from baobab_mtg_catalog.domain.value_objects.game_format import GameFormat
from baobab_mtg_catalog.domain.value_objects.legality_status import LegalityStatus


class TestFormatLegality:
    """Couple format + statut."""

    def test_to_mapping(self) -> None:
        """Sérialisation clé-valeur stable."""
        fl = FormatLegality(
            game_format=GameFormat.parse("pauper"),
            status=LegalityStatus.LEGAL,
        )
        assert fl.to_mapping() == {"format": "pauper", "status": "legal"}
