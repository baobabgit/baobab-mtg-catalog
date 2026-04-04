"""Tests pour :class:`SetQueryService`."""

from __future__ import annotations

from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services.set_query_service import SetQueryService


def test_set_query_get_by_code_and_scryfall(lea_catalog_facade: MtgCatalogFacade) -> None:
    """Lecture par code et par id Scryfall du set."""
    svc: SetQueryService = lea_catalog_facade.sets
    by_code = svc.get_by_code(SetCode.parse("lea"))
    by_scry = svc.get_by_scryfall_set_id(
        ScryfallId.parse("11111111-1111-4111-8111-111111111111"),
    )
    assert by_code.set_id == by_scry.set_id
