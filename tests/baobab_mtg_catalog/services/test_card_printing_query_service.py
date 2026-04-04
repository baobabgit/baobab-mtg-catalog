"""Tests pour :class:`CardPrintingQueryService`."""

from __future__ import annotations

from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services import CatalogDefinitionFilter, CatalogPrintingFilter
from baobab_mtg_catalog.services.card_printing_query_service import CardPrintingQueryService

from tests.baobab_mtg_catalog.services.scryfall_json_fixtures import bear_card_lea, set_payload_lea


def test_get_by_natural_key_scryfall_uuid(lea_catalog_facade: MtgCatalogFacade) -> None:
    """Résolution par clé naturelle Scryfall lorsque le payload porte ``id``."""
    svc: CardPrintingQueryService = lea_catalog_facade.printings
    scry = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
    p = svc.get_by_natural_key(scry)
    assert p.collector_number.value == "116"


def test_get_by_natural_key_triplet_when_no_scryfall_card_id() -> None:
    """Triplet set / collector / langue lorsque l'import n'a pas d'``id`` carte."""
    f = MtgCatalogFacade.in_memory()
    bear = dict(bear_card_lea())
    bear.pop("id", None)
    f.import_set_and_cards(set_payload_lea(), [bear])
    svc: CardPrintingQueryService = f.printings
    st = f.sets.get_by_code(SetCode.parse("lea"))
    key = (st.set_id, CollectorNumber.parse("5"), Language.EN)
    p = svc.get_by_natural_key(key)
    assert p.collector_number.value == "5"


def test_find_delegates_to_catalog(lea_catalog_facade: MtgCatalogFacade) -> None:
    """find() applique les mêmes règles que CatalogQueryService."""
    svc: CardPrintingQueryService = lea_catalog_facade.printings
    st = lea_catalog_facade.sets.get_by_code(SetCode.parse("lea"))
    got = svc.find(
        CatalogPrintingFilter(
            set_id=st.set_id,
            definition=CatalogDefinitionFilter(normalized_name_contains="bear"),
        ),
    )
    assert len(got) == 1
    assert got[0].collector_number.value == "5"
