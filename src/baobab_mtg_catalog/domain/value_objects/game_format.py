"""Identifiant de format de jeu construit (slug stable, ex.: ``standard``)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_game_format_error import InvalidGameFormatError

_SLUG_PATTERN: re.Pattern[str] = re.compile(r"^[a-z][a-z0-9_-]{1,47}$")


@dataclass(frozen=True, slots=True)
class GameFormat:
    """Slug minuscule identifiant un format (standard, commander, pauper, …).

    La validation est volontairement souple sur l'énumération des formats : de
    nouveaux formats Wizards peuvent apparaître ; seules la forme et la longueur
    sont contraintes ici.

    :param value: Slug normalisé.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _SLUG_PATTERN.fullmatch(normalized):
            raise InvalidGameFormatError(
                "Le format doit être un slug de 2 à 48 caractères, "
                "lettres minuscules, chiffres, tirets ou underscores "
                f"(reçu: {self.value!r})."
            )
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, raw: str) -> GameFormat:
        """Construit un identifiant de format à partir d'une entrée brute.

        :param raw: Slug potentiellement en casse mixte.
        :type raw: str
        :returns: Format normalisé.
        :rtype: GameFormat
        :raises InvalidGameFormatError: Si le slug est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: Slug du format.
        :rtype: str
        """
        return self.value
