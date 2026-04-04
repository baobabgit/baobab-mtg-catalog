"""Couleur de mana élémentaire (WUBRG) au sens Magic: The Gathering."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_color_error import InvalidColorError


class Color(StrEnum):
    """Représente une couleur de mana reconnue dans le domaine catalogue.

    Les valeurs sont les symboles usuels MTG (W, U, B, R, G). Ce type est
    volontairement minimal : le sans-couleur et les nuances de coût sont
    modélisés ailleurs (``ManaCost``, ``ColorIdentity``).

    :cvar WHITE: Blanc.
    :cvar BLUE: Bleu.
    :cvar BLACK: Noir.
    :cvar RED: Rouge.
    :cvar GREEN: Vert.
    """

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"

    @classmethod
    def parse(cls, raw: str) -> Color:
        """Construit une couleur à partir d'un symbole ou nom court.

        Accepte la lettre WUBRG en respectant la casse usuelle (insensible à la
        casse pour la lettre) ou le nom anglais complet de la couleur.

        :param raw: Entrée utilisateur (lettre WUBRG ou nom anglais, ex. w, white).
        :type raw: str
        :returns: Couleur normalisée.
        :rtype: Color
        :raises InvalidColorError: Si la valeur ne correspond à aucune couleur.
        """
        token = raw.strip()
        if not token:
            raise InvalidColorError("La couleur ne peut pas être vide.")
        upper = token.upper()
        if len(upper) == 1:
            try:
                return cls(upper)
            except ValueError as exc:
                raise InvalidColorError(f"Symbole de couleur inconnu: {raw!r}.") from exc
        aliases = {
            "WHITE": cls.WHITE,
            "BLUE": cls.BLUE,
            "BLACK": cls.BLACK,
            "RED": cls.RED,
            "GREEN": cls.GREEN,
        }
        key = upper.replace(" ", "_")
        if key in aliases:
            return aliases[key]
        raise InvalidColorError(f"Couleur non reconnue: {raw!r}.")
