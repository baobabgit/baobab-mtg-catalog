"""Rareté de printing au sens catalogue (hors logique de tirage produit)."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_rarity_error import InvalidRarityError


class Rarity(StrEnum):
    """Rareté métier alignée sur les catégories usuelles des données catalogue.

    :cvar COMMON: Commune.
    :cvar UNCOMMON: Peu commune.
    :cvar RARE: Rare.
    :cvar MYTHIC: Mythique.
    :cvar SPECIAL: Spéciale / variantes cataloguées ainsi.
    :cvar BONUS: Bonus (ex.: The List, certaines annexes).
    """

    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    MYTHIC = "mythic"
    SPECIAL = "special"
    BONUS = "bonus"

    @classmethod
    def parse(cls, raw: str) -> Rarity:
        """Interprète une rareté textuelle normalisée en minuscules.

        :param raw: Chaîne rareté (ex: ``\"rare\"``, ``\"mythic\"``).
        :type raw: str
        :returns: Valeur d'énumération correspondante.
        :rtype: Rarity
        :raises InvalidRarityError: Si la valeur est inconnue.
        """
        value = raw.strip().lower()
        if not value:
            raise InvalidRarityError("La rareté ne peut pas être vide.")
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidRarityError(f"Rareté inconnue: {raw!r}.") from exc
