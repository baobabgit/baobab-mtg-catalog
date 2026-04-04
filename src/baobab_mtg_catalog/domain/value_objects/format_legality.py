"""Association format de jeu + statut de légalité pour une entrée catalogue."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.game_format import GameFormat
from baobab_mtg_catalog.domain.value_objects.legality_status import LegalityStatus


@dataclass(frozen=True, slots=True)
class FormatLegality:
    """Couple (format, statut) décrivant la légalité dans un format construit.

    :param game_format: Format concerné.
    :type game_format: GameFormat
    :param status: Statut de légalité dans ce format.
    :type status: LegalityStatus
    """

    game_format: GameFormat
    status: LegalityStatus

    def to_mapping(self) -> dict[str, str]:
        """Représentation clé-valeur prête pour JSON ou journaux structurés.

        :returns: Dictionnaire avec clés ``format`` et ``status``.
        :rtype: dict[str, str]
        """
        return {"format": self.game_format.value, "status": self.status.value}
