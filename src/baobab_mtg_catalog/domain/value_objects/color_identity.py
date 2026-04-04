"""Identité de couleur (sous-ensemble WUBRG) pour le domaine catalogue."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.exceptions.invalid_color_identity_error import (
    InvalidColorIdentityError,
)

_WUBRG_ORDER: tuple[Color, ...] = (
    Color.WHITE,
    Color.BLUE,
    Color.BLACK,
    Color.RED,
    Color.GREEN,
)


@dataclass(frozen=True, slots=True)
class ColorIdentity:
    """Ensemble immuable de couleurs d'identité, ordonné logiquement en WUBRG.

    L'identité peut être vide (sans-couleur). Les doublons en entrée sont
    absorbés. L'ordre d'itération suit toujours WUBRG pour une sérialisation
    stable.

    :param colors: Couleurs composant l'identité.
    :type colors: frozenset[Color]
    """

    colors: frozenset[Color]

    def __post_init__(self) -> None:
        normalized = frozenset(self.colors)
        for item in normalized:
            if not isinstance(item, Color):
                raise InvalidColorIdentityError(
                    f"Élément d'identité de couleur invalide: {item!r}."
                )
        object.__setattr__(self, "colors", normalized)

    @classmethod
    def from_iterable(cls, colors: Iterable[Color]) -> ColorIdentity:
        """Construit une identité à partir d'un itérable (doublons ignorés).

        :param colors: Couleurs sources.
        :type colors: Iterable[Color]
        :returns: Identité normalisée.
        :rtype: ColorIdentity
        """
        return cls(frozenset(colors))

    @classmethod
    def empty(cls) -> ColorIdentity:
        """Identité vide (aucune couleur de mana dans l'identité)."""
        return cls(frozenset())

    def ordered_colors(self) -> tuple[Color, ...]:
        """Couleurs triées selon l'ordre WUBRG (sous-ensemble de cet ordre).

        :returns: Tuple stable pour affichage ou sérialisation.
        :rtype: tuple[Color, ...]
        """
        return tuple(color for color in _WUBRG_ORDER if color in self.colors)

    def is_empty(self) -> bool:
        """Indique si l'identité ne contient aucune couleur."""
        return len(self.colors) == 0

    def __iter__(self) -> Iterator[Color]:
        return iter(self.ordered_colors())

    def to_primitive(self) -> list[str]:
        """Représentation JSON-friendly (liste de symboles WUBRG triés).

        :returns: Liste de chaînes ``\"W\"``, ``\"U\"``, etc.
        :rtype: list[str]
        """
        return [c.value for c in self.ordered_colors()]
