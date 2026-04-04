"""Code d'extension (set) stable, tel qu'utilisé pour indexer un printing."""

from __future__ import annotations

import re
from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_set_code_error import InvalidSetCodeError

_SET_CODE_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z0-9]{1,8}$")


@dataclass(frozen=True, slots=True)
class SetCode:
    """Code set alphanumérique en majuscules (ex: ``ONE``, ``MH2``).

    La longueur est bornée pour rester compatible avec les usages MTG courants
    tout en évitant des chaînes arbitrairement longues.

    :param value: Code normalisé en majuscules.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        if not _SET_CODE_PATTERN.fullmatch(normalized):
            raise InvalidSetCodeError(
                "Le code de set doit contenir 1 à 8 caractères alphanumériques "
                f"ASCII (reçu: {self.value!r})."
            )
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, raw: str) -> SetCode:
        """Construit un ``SetCode`` à partir d'une entrée brute.

        :param raw: Code potentiellement mixte casse.
        :type raw: str
        :returns: Code normalisé.
        :rtype: SetCode
        :raises InvalidSetCodeError: Si le format est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Valeur primitive sérialisable (code en majuscules).

        :returns: Chaîne du code set.
        :rtype: str
        """
        return self.value
