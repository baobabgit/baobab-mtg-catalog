"""Statut de légalité d'une carte dans un format de jeu construit."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_legality_status_error import (
    InvalidLegalityStatusError,
)


class LegalityStatus(StrEnum):
    """Valeurs usuelles de légalité dans les données catalogue MTG.

    :cvar LEGAL: Légal en nombre illimité.
    :cvar NOT_LEGAL: Non légal dans le format.
    :cvar BANNED: Banni.
    :cvar RESTRICTED: Restreint (au plus une copie en Vintage).
    """

    LEGAL = "legal"
    NOT_LEGAL = "not_legal"
    BANNED = "banned"
    RESTRICTED = "restricted"

    @classmethod
    def parse(cls, raw: str) -> LegalityStatus:
        """Interprète un statut textuel normalisé en snake_case.

        :param raw: Statut (ex: ``\"not_legal\"``, ``\"banned\"``).
        :type raw: str
        :returns: Statut connu.
        :rtype: LegalityStatus
        :raises InvalidLegalityStatusError: Si la valeur est inconnue.
        """
        value = raw.strip().lower()
        if not value:
            raise InvalidLegalityStatusError("Le statut de légalité ne peut pas être vide.")
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidLegalityStatusError(f"Statut de légalité inconnu: {raw!r}.") from exc
