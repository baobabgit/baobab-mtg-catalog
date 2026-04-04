"""Face d'une carte logique (texte face avant, verso ou segment d'un MDFC)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.card_definitions.validation_utils import (
    validate_optional_pt_loyalty,
    validate_text_field,
)
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.exceptions.invalid_card_face_error import InvalidCardFaceError

_MAX_NAME_LEN: int = 500
_MAX_ORACLE_LEN: int = 8000


@dataclass(frozen=True, slots=True)
class CardFace:
    """Une face textuelle / jeu d'une carte logique.

    Ne contient aucun attribut d'impression (set, collector number, finition).

    :param name: Nom de la face telle qu'affichée.
    :type name: str
    :param normalized_name: Nom normalisé pour recherche / index (ex. minuscules).
    :type normalized_name: str
    :param mana_cost: Coût de mana de cette face.
    :type mana_cost: ManaCost
    :param type_line: Ligne de types de cette face.
    :type type_line: CardTypeLine
    :param oracle_text: Texte oracle de cette face (peut être vide).
    :type oracle_text: str
    :param colors: Couleurs de mana présentes sur cette face (symboles dans le coût).
    :type colors: frozenset[Color]
    :param power: Force, si la face est une créature ou utilise P/T.
    :type power: str | None
    :param toughness: Endurance, si applicable.
    :type toughness: str | None
    :param loyalty: Loyauté planeswalker, si applicable.
    :type loyalty: str | None
    """

    name: str
    normalized_name: str
    mana_cost: ManaCost
    type_line: CardTypeLine
    oracle_text: str
    colors: frozenset[Color]
    power: str | None = None
    toughness: str | None = None
    loyalty: str | None = None

    def __post_init__(self) -> None:
        name = validate_text_field(
            self.name,
            label="Le nom de face",
            max_len=_MAX_NAME_LEN,
            allow_empty=False,
            exc_cls=InvalidCardFaceError,
        )
        norm = validate_text_field(
            self.normalized_name,
            label="Le nom normalisé de face",
            max_len=_MAX_NAME_LEN,
            allow_empty=False,
            exc_cls=InvalidCardFaceError,
        )
        oracle = validate_text_field(
            self.oracle_text,
            label="Le texte oracle de face",
            max_len=_MAX_ORACLE_LEN,
            allow_empty=True,
            exc_cls=InvalidCardFaceError,
        )
        colors = frozenset(self.colors)
        for c in colors:
            if not isinstance(c, Color):
                raise InvalidCardFaceError(f"Couleur de face invalide: {c!r}.")
        power = validate_optional_pt_loyalty(
            self.power, label="La force", exc_cls=InvalidCardFaceError
        )
        toughness = validate_optional_pt_loyalty(
            self.toughness, label="L'endurance", exc_cls=InvalidCardFaceError
        )
        loyalty = validate_optional_pt_loyalty(
            self.loyalty, label="La loyauté", exc_cls=InvalidCardFaceError
        )
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "normalized_name", norm)
        object.__setattr__(self, "oracle_text", oracle)
        object.__setattr__(self, "colors", colors)
        object.__setattr__(self, "power", power)
        object.__setattr__(self, "toughness", toughness)
        object.__setattr__(self, "loyalty", loyalty)
