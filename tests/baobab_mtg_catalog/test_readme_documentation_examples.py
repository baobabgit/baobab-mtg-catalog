"""Non-régression des parcours documentés dans le README (adaptateurs, import, consultation)."""

from __future__ import annotations

from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.adapters.scryfall import (
    ScryfallCardDefinitionAdapter,
    ScryfallCardPrintingAdapter,
    ScryfallSetAdapter,
)
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services import CatalogDefinitionFilter, CatalogPrintingFilter

from .services.scryfall_json_fixtures import bear_card_lea, mono_card_lightning_lea, set_payload_lea


def test_readme_scryfall_adapter_path_set_definition_printing() -> None:
    """Même enchaînement que l'exemple README : adaptateurs sur payloads type Scryfall."""
    set_id = SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    st = ScryfallSetAdapter.to_set(set_payload_lea(), set_id=set_id)
    assert st.code.value == "LEA"

    definition_id = CardDefinitionIdentifier.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
    definition = ScryfallCardDefinitionAdapter.to_card_definition(
        mono_card_lightning_lea(),
        card_definition_id=definition_id,
    )
    assert definition.oracle_id.value == "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"

    printing_id = CardPrintingIdentifier.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
    printing = ScryfallCardPrintingAdapter.to_card_printing(
        mono_card_lightning_lea(),
        card_printing_id=printing_id,
        card_definition_id=definition.card_definition_id,
        set_id=st.set_id,
    )
    assert printing.set_id == st.set_id
    assert printing.scryfall_printing_id is not None
    assert printing.scryfall_printing_id.value == "dddddddd-dddd-4ddd-8ddd-dddddddddddd"


def test_readme_idempotent_import_and_catalog_queries() -> None:
    """Import idempotent via façade puis consultation (filtres métier)."""
    facade = MtgCatalogFacade.in_memory()
    facade.import_set_and_cards(
        set_payload_lea(),
        [mono_card_lightning_lea(), bear_card_lea()],
    )
    facade.import_set_and_cards(
        set_payload_lea(),
        [mono_card_lightning_lea(), bear_card_lea()],
    )

    bolts = facade.catalog.find_definitions(
        CatalogDefinitionFilter(normalized_name_contains="bolt"),
    )
    assert len(bolts) == 1

    st = facade.sets.get_by_code(SetCode.parse("lea"))

    in_set = facade.printings.find_in_set(
        st.set_id,
        CatalogPrintingFilter(definition=CatalogDefinitionFilter(normalized_name_contains="bear")),
    )
    assert len(in_set) == 1
    assert in_set[0].collector_number.value == "5"
