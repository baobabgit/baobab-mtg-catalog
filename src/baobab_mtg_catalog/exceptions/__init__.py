"""Exceptions spécifiques au package ``baobab_mtg_catalog``."""

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)
from baobab_mtg_catalog.exceptions.card_definition_not_found_error import (
    CardDefinitionNotFoundError,
)
from baobab_mtg_catalog.exceptions.card_printing_not_found_error import (
    CardPrintingNotFoundError,
)
from baobab_mtg_catalog.exceptions.catalog_import_batch_set_mismatch_error import (
    CatalogImportBatchSetMismatchError,
)
from baobab_mtg_catalog.exceptions.catalog_import_inconsistency_error import (
    CatalogImportInconsistencyError,
)
from baobab_mtg_catalog.exceptions.catalog_import_printing_definition_mismatch_error import (
    CatalogImportPrintingDefinitionMismatchError,
)
from baobab_mtg_catalog.exceptions.catalog_import_set_scryfall_mismatch_error import (
    CatalogImportSetScryfallMismatchError,
)
from baobab_mtg_catalog.exceptions.invalid_card_definition_error import (
    InvalidCardDefinitionError,
)
from baobab_mtg_catalog.exceptions.invalid_card_definition_identifier_error import (
    InvalidCardDefinitionIdentifierError,
)
from baobab_mtg_catalog.exceptions.invalid_card_face_error import InvalidCardFaceError
from baobab_mtg_catalog.exceptions.invalid_card_printing_error import (
    InvalidCardPrintingError,
)
from baobab_mtg_catalog.exceptions.invalid_card_printing_identifier_error import (
    InvalidCardPrintingIdentifierError,
)
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
from baobab_mtg_catalog.exceptions.invalid_payload_error import InvalidPayloadError
from baobab_mtg_catalog.exceptions.invalid_oracle_id_error import InvalidOracleIdError
from baobab_mtg_catalog.exceptions.invalid_rarity_error import InvalidRarityError
from baobab_mtg_catalog.exceptions.invalid_scryfall_id_error import InvalidScryfallIdError
from baobab_mtg_catalog.exceptions.invalid_set_code_error import InvalidSetCodeError
from baobab_mtg_catalog.exceptions.invalid_set_error import InvalidSetError
from baobab_mtg_catalog.exceptions.invalid_set_id_error import InvalidSetIdError
from baobab_mtg_catalog.exceptions.invalid_set_type_error import InvalidSetTypeError
from baobab_mtg_catalog.exceptions.mapping_error import MappingError
from baobab_mtg_catalog.exceptions.normalization_error import NormalizationError
from baobab_mtg_catalog.exceptions.repository_entity_conflict_error import (
    RepositoryEntityConflictError,
)
from baobab_mtg_catalog.exceptions.set_not_found_error import SetNotFoundError

__all__: list[str] = [
    "BaobabMtgCatalogException",
    "CardDefinitionNotFoundError",
    "CardPrintingNotFoundError",
    "CatalogImportBatchSetMismatchError",
    "CatalogImportInconsistencyError",
    "CatalogImportPrintingDefinitionMismatchError",
    "CatalogImportSetScryfallMismatchError",
    "InvalidCardDefinitionError",
    "InvalidCardDefinitionIdentifierError",
    "InvalidCardFaceError",
    "InvalidCardPrintingError",
    "InvalidCardPrintingIdentifierError",
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
    "InvalidPayloadError",
    "InvalidRarityError",
    "InvalidScryfallIdError",
    "InvalidSetCodeError",
    "InvalidSetError",
    "InvalidSetIdError",
    "InvalidSetTypeError",
    "MappingError",
    "NormalizationError",
    "RepositoryEntityConflictError",
    "SetNotFoundError",
]
