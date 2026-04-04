"""Exceptions spécifiques au package ``baobab_mtg_catalog``."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)
from baobab_mtg_catalog.exceptions.invalid_card_definition_error import (
    InvalidCardDefinitionError,
)
from baobab_mtg_catalog.exceptions.invalid_card_definition_identifier_error import (
    InvalidCardDefinitionIdentifierError,
)
from baobab_mtg_catalog.exceptions.invalid_card_face_error import InvalidCardFaceError
from baobab_mtg_catalog.exceptions.invalid_card_type_line_error import (
    InvalidCardTypeLineError,
)
from baobab_mtg_catalog.exceptions.invalid_collector_number_error import (
    InvalidCollectorNumberError,
)
from baobab_mtg_catalog.exceptions.invalid_color_error import InvalidColorError
from baobab_mtg_catalog.exceptions.invalid_color_identity_error import (
    InvalidColorIdentityError,
)
from baobab_mtg_catalog.exceptions.invalid_domain_value_error import (
    InvalidDomainValueError,
)
from baobab_mtg_catalog.exceptions.invalid_finish_error import InvalidFinishError
from baobab_mtg_catalog.exceptions.invalid_game_format_error import (
    InvalidGameFormatError,
)
from baobab_mtg_catalog.exceptions.invalid_language_error import InvalidLanguageError
from baobab_mtg_catalog.exceptions.invalid_legality_status_error import (
    InvalidLegalityStatusError,
)
from baobab_mtg_catalog.exceptions.invalid_mana_cost_error import InvalidManaCostError
from baobab_mtg_catalog.exceptions.invalid_multiverse_id_error import (
    InvalidMultiverseIdError,
)
from baobab_mtg_catalog.exceptions.invalid_oracle_id_error import InvalidOracleIdError
from baobab_mtg_catalog.exceptions.invalid_rarity_error import InvalidRarityError
from baobab_mtg_catalog.exceptions.invalid_scryfall_id_error import InvalidScryfallIdError
from baobab_mtg_catalog.exceptions.invalid_set_code_error import InvalidSetCodeError
from baobab_mtg_catalog.exceptions.invalid_set_error import InvalidSetError
from baobab_mtg_catalog.exceptions.invalid_set_id_error import InvalidSetIdError
from baobab_mtg_catalog.exceptions.invalid_set_type_error import InvalidSetTypeError

__all__: list[str] = [
    "BaobabMtgCatalogException",
    "InvalidCardDefinitionError",
    "InvalidCardDefinitionIdentifierError",
    "InvalidCardFaceError",
    "InvalidCardTypeLineError",
    "InvalidCollectorNumberError",
    "InvalidColorError",
    "InvalidColorIdentityError",
    "InvalidDomainValueError",
    "InvalidFinishError",
    "InvalidGameFormatError",
    "InvalidLanguageError",
    "InvalidLegalityStatusError",
    "InvalidManaCostError",
    "InvalidMultiverseIdError",
    "InvalidOracleIdError",
    "InvalidRarityError",
    "InvalidScryfallIdError",
    "InvalidSetCodeError",
    "InvalidSetError",
    "InvalidSetIdError",
    "InvalidSetTypeError",
]
