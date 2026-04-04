"""Entité domaine : carte logique (oracle), indépendante des impressions."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_definitions.card_face import CardFace
from baobab_mtg_catalog.domain.card_definitions.validation_utils import (
    validate_optional_pt_loyalty,
    validate_text_field,
)
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions.invalid_card_definition_error import (
    InvalidCardDefinitionError,
)

_MAX_NAME_LEN: int = 500
_MAX_ORACLE_LEN: int = 8000
_MAX_KEYWORD_LEN: int = 48


def _normalize_keywords(
    raw: frozenset[str],
    *,
    exc_cls: type[InvalidCardDefinitionError],
) -> frozenset[str]:
    result: set[str] = set()
    for item in raw:
        kw = item.strip().lower()
        if not kw:
            raise exc_cls("Un mot-clé vide n'est pas autorisé.")
        if len(kw) > _MAX_KEYWORD_LEN:
            raise exc_cls(f"Mot-clé trop long: {item!r}.")
        result.add(kw)
    return frozenset(result)


def _mono_face_aligns_with_card_fields(  # pylint: disable=too-many-arguments
    face: CardFace,
    *,
    name: str,
    normalized_name: str,
    type_line: CardTypeLine,
    oracle_text: str,
    colors: frozenset[Color],
    power: str | None,
    toughness: str | None,
    loyalty: str | None,
) -> bool:
    """Vérifie l'alignement strict entre l'unique face et les champs agrégés carte."""
    return (
        face.name == name
        and face.normalized_name == normalized_name
        and face.type_line == type_line
        and face.oracle_text == oracle_text
        and face.colors == colors
        and face.power == power
        and face.toughness == toughness
        and face.loyalty == loyalty
    )


@dataclass(frozen=True, slots=True)
class CardDefinition:  # pylint: disable=too-many-instance-attributes
    """Carte logique au sens Oracle, partagée par toutes ses impressions.

    **Identité d'entité** : égalité et hachage sur :class:`CardDefinitionIdentifier`
    (UUID métier géré par la persistance).

    **Idempotence d'import** : la clé naturelle est l':class:`OracleId`
    (:meth:`natural_key`), stable pour une même carte entre extensions et
    printings. Les identifiants optionnels ``scryfall_card_id`` et
    ``multiverse_id`` aident les adaptateurs sans coupler le domaine au JSON
    Scryfall.

    **Mono-face** : une seule :class:`CardFace` ; champs agrégés (nom, coût,
    types, texte, couleurs, P/T, loyauté) doivent coïncider avec cette face.

    **Multi-face** (MDFC, split, etc.) : plusieurs faces ; ``power``,
    ``toughness`` et ``loyalty`` au niveau carte doivent être ``None`` (définis
    par face).

    :param card_definition_id: Identifiant métier (UUID).
    :type card_definition_id: CardDefinitionIdentifier
    :param oracle_id: Identifiant oracle stable (clé naturelle métier).
    :type oracle_id: OracleId
    :param name: Nom complet affiché (ex. ``A // B`` pour un MDFC).
    :type name: str
    :param normalized_name: Nom normalisé pour recherche.
    :type normalized_name: str
    :param mana_cost: Coût de mana principal (face initiale).
    :type mana_cost: ManaCost
    :param mana_value: Valeur de mana convertie (CMC) non négative.
    :type mana_value: float
    :param type_line: Ligne de types agrégée ou de la face principale.
    :type type_line: CardTypeLine
    :param oracle_text: Texte oracle agrégé ou de la face principale.
    :type oracle_text: str
    :param colors: Couleurs de mana de la carte (agrégat usuel).
    :type colors: frozenset[Color]
    :param color_identity: Identité couleur pour formats construits.
    :type color_identity: ColorIdentity
    :param faces: Faces non vides, ordre jeu (face avant en premier).
    :type faces: tuple[CardFace, ...]
    :param keywords: Mots-clé normalisés en minuscules.
    :type keywords: frozenset[str]
    :param power: Force au niveau carte (mono-face typiquement).
    :type power: str | None
    :param toughness: Endurance au niveau carte (mono-face typiquement).
    :type toughness: str | None
    :param loyalty: Loyauté au niveau carte (mono-face typiquement).
    :type loyalty: str | None
    :param scryfall_card_id: Corrélation optionnelle vers un id Scryfall carte.
    :type scryfall_card_id: ScryfallId | None
    :param multiverse_id: Identifiant Gatherer optionnel.
    :type multiverse_id: MultiverseId | None
    """

    card_definition_id: CardDefinitionIdentifier
    oracle_id: OracleId
    name: str
    normalized_name: str
    mana_cost: ManaCost
    mana_value: float
    type_line: CardTypeLine
    oracle_text: str
    colors: frozenset[Color]
    color_identity: ColorIdentity
    faces: tuple[CardFace, ...]
    keywords: frozenset[str] = frozenset()
    power: str | None = None
    toughness: str | None = None
    loyalty: str | None = None
    scryfall_card_id: ScryfallId | None = None
    multiverse_id: MultiverseId | None = None

    def __post_init__(self) -> None:
        if not self.faces:
            raise InvalidCardDefinitionError("Une carte doit avoir au moins une face.")
        name = validate_text_field(
            self.name,
            label="Le nom de la carte",
            max_len=_MAX_NAME_LEN,
            allow_empty=False,
            exc_cls=InvalidCardDefinitionError,
        )
        norm = validate_text_field(
            self.normalized_name,
            label="Le nom normalisé",
            max_len=_MAX_NAME_LEN,
            allow_empty=False,
            exc_cls=InvalidCardDefinitionError,
        )
        oracle = validate_text_field(
            self.oracle_text,
            label="Le texte oracle",
            max_len=_MAX_ORACLE_LEN,
            allow_empty=True,
            exc_cls=InvalidCardDefinitionError,
        )
        if self.mana_value < 0 or self.mana_value != self.mana_value:
            raise InvalidCardDefinitionError(
                f"La valeur de mana doit être un nombre réel >= 0 (reçu: {self.mana_value})."
            )
        colors = frozenset(self.colors)
        for c in colors:
            if not isinstance(c, Color):
                raise InvalidCardDefinitionError(f"Couleur invalide: {c!r}.")
        keywords = _normalize_keywords(self.keywords, exc_cls=InvalidCardDefinitionError)
        power = validate_optional_pt_loyalty(
            self.power, label="La force", exc_cls=InvalidCardDefinitionError
        )
        toughness = validate_optional_pt_loyalty(
            self.toughness, label="L'endurance", exc_cls=InvalidCardDefinitionError
        )
        loyalty = validate_optional_pt_loyalty(
            self.loyalty, label="La loyauté", exc_cls=InvalidCardDefinitionError
        )
        if self.mana_cost != self.faces[0].mana_cost:
            raise InvalidCardDefinitionError(
                "Le coût de mana de la carte doit correspondre à celui de la première face."
            )
        face_count = len(self.faces)
        if face_count >= 2:
            if power is not None or toughness is not None or loyalty is not None:
                raise InvalidCardDefinitionError(
                    "Pour une carte multi-face, force, endurance et loyauté carte "
                    "doivent être absentes (définies par face)."
                )
        if face_count == 1:
            face = self.faces[0]
            if not _mono_face_aligns_with_card_fields(
                face,
                name=name,
                normalized_name=norm,
                type_line=self.type_line,
                oracle_text=oracle,
                colors=colors,
                power=power,
                toughness=toughness,
                loyalty=loyalty,
            ):
                raise InvalidCardDefinitionError(
                    "Pour une carte mono-face, les champs carte et face doivent être alignés."
                )
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "normalized_name", norm)
        object.__setattr__(self, "oracle_text", oracle)
        object.__setattr__(self, "colors", colors)
        object.__setattr__(self, "keywords", keywords)
        object.__setattr__(self, "power", power)
        object.__setattr__(self, "toughness", toughness)
        object.__setattr__(self, "loyalty", loyalty)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CardDefinition):
            return NotImplemented
        return self.card_definition_id == other.card_definition_id

    def __hash__(self) -> int:
        return hash(self.card_definition_id)

    @property
    def primary_face(self) -> CardFace:
        """Première face dans l'ordre jeu (face avant / segment principal).

        :returns: Face initiale.
        :rtype: CardFace
        """
        return self.faces[0]

    def is_multi_faced(self) -> bool:
        """Indique si la carte possède plusieurs faces texte."""
        return len(self.faces) > 1

    def natural_key(self) -> OracleId:
        """Clé naturelle pour fusionner un import sur une définition existante.

        :returns: Oracle id stable.
        :rtype: OracleId
        """
        return self.oracle_id

    def same_logical_card_as(self, other: CardDefinition) -> bool:
        """Indique si deux définitions désignent la même carte Oracle.

        :param other: Autre définition.
        :type other: CardDefinition
        :returns: Vrai si les oracle id sont identiques.
        :rtype: bool
        """
        return self.oracle_id == other.oracle_id
