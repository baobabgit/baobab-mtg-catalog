"""Objets de valeur partagés du domaine catalogue MTG."""

from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.format_legality import FormatLegality
from baobab_mtg_catalog.domain.value_objects.game_format import GameFormat
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.legality_status import LegalityStatus
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode

__all__: list[str] = [
    "CardTypeLine",
    "CollectorNumber",
    "Color",
    "ColorIdentity",
    "Finish",
    "FormatLegality",
    "GameFormat",
    "Language",
    "LegalityStatus",
    "ManaCost",
    "MultiverseId",
    "OracleId",
    "Rarity",
    "ScryfallId",
    "SetCode",
]
