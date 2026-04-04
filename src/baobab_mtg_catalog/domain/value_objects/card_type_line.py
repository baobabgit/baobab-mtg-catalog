"""Ligne de type Oracle (types et sous-types) pour une face de carte."""

from __future__ import annotations

import re
from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_card_type_line_error import (
    InvalidCardTypeLineError,
)

_CONTROL_CHARS: re.Pattern[str] = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_MAX_LENGTH: int = 512


@dataclass(frozen=True, slots=True)
class CardTypeLine:
    """Texte de type ligne tel qu'affiché sur la carte (côté domaine).

    Le contenu sémantique (creature, legendary, etc.) n'est pas décomposé ici :
    cette valeur sert de libellé stable, filtrable et affichable. Un découpage
    fin pourra être introduit dans une feature ultérieure si nécessaire.

    :param value: Ligne de types complète.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise InvalidCardTypeLineError("La ligne de type ne peut pas être vide.")
        if len(normalized) > _MAX_LENGTH:
            raise InvalidCardTypeLineError(
                f"La ligne de type dépasse {_MAX_LENGTH} caractères: {self.value!r}."
            )
        if _CONTROL_CHARS.search(normalized):
            raise InvalidCardTypeLineError("La ligne de type contient des caractères de contrôle.")
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, raw: str) -> CardTypeLine:
        """Construit une ligne de type à partir d'une entrée brute.

        :param raw: Texte Oracle brut.
        :type raw: str
        :returns: Ligne validée.
        :rtype: CardTypeLine
        :raises InvalidCardTypeLineError: Si la valeur est rejetée.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: Ligne de type.
        :rtype: str
        """
        return self.value
