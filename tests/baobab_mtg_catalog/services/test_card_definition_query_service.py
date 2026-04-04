"""Tests pour :class:`CardDefinitionQueryService`."""

from __future__ import annotations

from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services.card_definition_query_service import CardDefinitionQueryService


def test_list_by_normalized_name_exact(lea_catalog_facade: MtgCatalogFacade) -> None:
    """Égalité stricte sur le nom normalisé."""
    svc: CardDefinitionQueryService = lea_catalog_facade.definitions
    got = svc.list_by_normalized_name("lightning bolt")
    assert len(got) == 1
    assert got[0].name == "Lightning Bolt"


def test_list_for_set_dedupes_definitions(lea_catalog_facade: MtgCatalogFacade) -> None:
    """Deux printings → deux définitions distinctes listées une fois chacune."""
    svc: CardDefinitionQueryService = lea_catalog_facade.definitions
    st = lea_catalog_facade.sets.get_by_code(SetCode.parse("lea"))
    defs = svc.list_for_set(st.set_id)
    assert len(defs) == 2
    names = sorted(d.normalized_name for d in defs)
    assert names == ["grizzly bears", "lightning bolt"]
