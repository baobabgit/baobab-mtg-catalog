"""Adaptateur Scryfall JSON → :class:`CardPrinting`."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from baobab_mtg_catalog.adapters.scryfall.scryfall_normalize import (
    finishes_from_scryfall,
    image_uris_from_scryfall,
    language_from_scryfall,
    optional_multiverse_id,
    optional_scryfall_id,
    parse_iso_date_optional,
    rarity_from_scryfall,
    run_mapping,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import optional_str, require_str
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber


class ScryfallCardPrintingAdapter:
    """Transforme un objet ``card`` Scryfall en :class:`CardPrinting`.

    Le même payload carte sert côté Scryfall à la fois aux aspects Oracle et
    printing ; cet adaptateur ne conserve que les champs propres à l'impression.
    """

    @staticmethod
    def to_card_printing(
        payload: Mapping[str, Any],
        *,
        card_printing_id: CardPrintingIdentifier,
        card_definition_id: CardDefinitionIdentifier,
        set_id: SetId,
    ) -> CardPrinting:
        """Construit un printing depuis un payload carte Scryfall.

        :param payload: Objet carte JSON Scryfall.
        :param card_printing_id: Identifiant métier printing.
        :param card_definition_id: Lien vers la définition Oracle importée.
        :param set_id: Lien vers le set métier déjà résolu.
        :returns: Impression normalisée.
        :raises InvalidPayloadError: Si la structure minimale est absente.
        :raises NormalizationError: Si une valeur est incohérente.
        :raises MappingError: Si le domaine rejette le résultat.
        """
        lang_raw = optional_str(payload, "lang") or "en"
        language = language_from_scryfall(lang_raw)
        rarity = rarity_from_scryfall(require_str(payload, "rarity"))
        finishes = finishes_from_scryfall(payload.get("finishes"))
        collector_number = run_mapping(
            "collector_number",
            lambda: CollectorNumber.parse(require_str(payload, "collector_number")),
        )
        artist = optional_str(payload, "artist")
        released_at = parse_iso_date_optional(payload.get("released_at"), field="released_at")
        scryfall_printing_id = optional_scryfall_id(payload, "id")
        multiverse_id = optional_multiverse_id(payload)
        image_uris = image_uris_from_scryfall(payload)
        return run_mapping(
            "CardPrinting",
            lambda: CardPrinting(
                card_printing_id=card_printing_id,
                card_definition_id=card_definition_id,
                set_id=set_id,
                collector_number=collector_number,
                language=language,
                rarity=rarity,
                finishes=finishes,
                artist=artist,
                image_uris=image_uris,
                released_at=released_at,
                scryfall_printing_id=scryfall_printing_id,
                multiverse_id=multiverse_id,
            ),
        )
