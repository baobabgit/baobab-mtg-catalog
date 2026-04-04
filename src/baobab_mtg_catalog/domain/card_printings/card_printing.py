"""Entité domaine : impression concrète d'une carte dans un set."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_definitions.validation_utils import validate_text_field
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.printing_image_uris import PrintingImageUris
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.exceptions.invalid_card_printing_error import InvalidCardPrintingError

_MAX_ARTIST_LEN: int = 500
_EARLIEST_RELEASE_YEAR: int = 1993
_LATEST_RELEASE_YEAR: int = 2100


@dataclass(frozen=True, slots=True)
class CardPrinting:  # pylint: disable=too-many-instance-attributes
    """Impression catalogue : une carte précise dans une extension et une langue.

    **Identité d'entité** : égalité et hachage sur :class:`CardPrintingIdentifier`
    (UUID métier attribué par la persistance).

    **Idempotence d'import** : :meth:`natural_key` privilégie
    ``scryfall_printing_id`` lorsqu'il est présent (id carte Scryfall par
    printing). Sinon la clé de repli est le triplet ``(set_id,
    collector_number, language)`` pour corréler des sources sans UUID
    fournisseur.

    Aucune logique d'inventaire, de possession ou d'import n'est portée par ce
    modèle : uniquement des faits sur une impression.

    :param card_printing_id: Identifiant métier (UUID).
    :type card_printing_id: CardPrintingIdentifier
    :param card_definition_id: Définition Oracle concernée.
    :type card_definition_id: CardDefinitionIdentifier
    :param set_id: Extension d'appartenance.
    :type set_id: SetId
    :param collector_number: Numéro de collection sur la carte.
    :type collector_number: CollectorNumber
    :param language: Langue du texte / de l'impression.
    :type language: Language
    :param rarity: Rareté catalogue de ce printing.
    :type rarity: Rarity
    :param finishes: Finitions disponibles pour ce printing (non vide).
    :type finishes: frozenset[Finish]
    :param artist: Crédit illustrateur si connu.
    :type artist: str | None
    :param image_uris: Liens vers les visuels numériques, si connus.
    :type image_uris: PrintingImageUris | None
    :param released_at: Date de disponibilité / sortie du printing si connue.
    :type released_at: date | None
    :param scryfall_printing_id: Identifiant Scryfall de la carte (printing).
    :type scryfall_printing_id: ScryfallId | None
    :param multiverse_id: Identifiant Gatherer optionnel.
    :type multiverse_id: MultiverseId | None
    """

    card_printing_id: CardPrintingIdentifier
    card_definition_id: CardDefinitionIdentifier
    set_id: SetId
    collector_number: CollectorNumber
    language: Language
    rarity: Rarity
    finishes: frozenset[Finish]
    artist: str | None = None
    image_uris: PrintingImageUris | None = None
    released_at: date | None = None
    scryfall_printing_id: ScryfallId | None = None
    multiverse_id: MultiverseId | None = None

    def __post_init__(self) -> None:
        if not self.finishes:
            raise InvalidCardPrintingError(
                "Un printing doit exposer au moins une finition disponible."
            )
        finishes_set = frozenset(self.finishes)
        for fin in finishes_set:
            if not isinstance(fin, Finish):
                raise InvalidCardPrintingError(f"Finition invalide: {fin!r}.")
        artist_norm: str | None
        if self.artist is None:
            artist_norm = None
        else:
            artist_text = validate_text_field(
                self.artist,
                label="Le nom d'artiste",
                max_len=_MAX_ARTIST_LEN,
                allow_empty=True,
                exc_cls=InvalidCardPrintingError,
            )
            artist_norm = artist_text if artist_text else None
        if self.released_at is not None:
            year = self.released_at.year
            if year < _EARLIEST_RELEASE_YEAR or year > _LATEST_RELEASE_YEAR:
                raise InvalidCardPrintingError(
                    "La date de sortie du printing est hors plausibilité: " f"{self.released_at!r}."
                )
        object.__setattr__(self, "finishes", finishes_set)
        object.__setattr__(self, "artist", artist_norm)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CardPrinting):
            return NotImplemented
        return self.card_printing_id == other.card_printing_id

    def __hash__(self) -> int:
        return hash(self.card_printing_id)

    def natural_key(
        self,
    ) -> ScryfallId | tuple[SetId, CollectorNumber, Language]:
        """Clé naturelle pour fusionner un import avec un printing existant.

        :returns: Identifiant Scryfall du printing ou triplet local de repli.
        :rtype: ScryfallId | tuple[SetId, CollectorNumber, Language]
        """
        if self.scryfall_printing_id is not None:
            return self.scryfall_printing_id
        return (self.set_id, self.collector_number, self.language)

    def same_catalog_printing_as(self, other: CardPrinting) -> bool:
        """Indique si deux impressions correspondent à la même entrée catalogue.

        Compare les :meth:`natural_key` des deux instances.

        :param other: Autre printing.
        :type other: CardPrinting
        :returns: Vrai si les clés naturelles coïncident.
        :rtype: bool
        """
        return self.natural_key() == other.natural_key()
