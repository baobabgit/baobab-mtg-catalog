"""Numéro de collection tel qu'imprimé sur la carte (peut être alphanumérique)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_collector_number_error import (
    InvalidCollectorNumberError,
)

_COLLECTOR_PATTERN: re.Pattern[str] = re.compile(r"^[A-Za-z0-9\u2605\u2217\u2606\u2726/\-–]+$")
_MAX_LENGTH: int = 64


@dataclass(frozen=True, slots=True)
class CollectorNumber:
    """Numéro de collection conservé tel quel pour préserver les zéros initiaux.

    Autorise lettres, chiffres, tirets, barres obliques et quelques glyphes
    spéciaux usuels (étoiles) rencontrés sur certaines cartes promo.

    :param value: Numéro tel qu'affiché sur la carte / dans le catalogue.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise InvalidCollectorNumberError("Le numéro de collection ne peut pas être vide.")
        if len(normalized) > _MAX_LENGTH:
            raise InvalidCollectorNumberError(
                f"Le numéro de collection est trop long (>{_MAX_LENGTH}): {self.value!r}."
            )
        if not _COLLECTOR_PATTERN.fullmatch(normalized):
            raise InvalidCollectorNumberError(
                f"Le numéro de collection contient des caractères interdits: {self.value!r}."
            )
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, raw: str) -> CollectorNumber:
        """Construit un numéro de collection à partir d'une entrée brute.

        :param raw: Valeur brute (espaces de tête / fin ignorés).
        :type raw: str
        :returns: Numéro validé.
        :rtype: CollectorNumber
        :raises InvalidCollectorNumberError: Si la valeur est rejetée.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: Numéro de collection.
        :rtype: str
        """
        return self.value
