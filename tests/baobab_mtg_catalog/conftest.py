"""Fixtures pytest partagées pour le package ``baobab_mtg_catalog``."""

from __future__ import annotations

import pytest

from baobab_mtg_catalog import MtgCatalogFacade

from .services.scryfall_json_fixtures import bear_card_lea, mono_card_lightning_lea, set_payload_lea


@pytest.fixture
def lea_catalog_facade() -> MtgCatalogFacade:
    """Façade in-memory après import LEA + Lightning Bolt + Grizzly Bears."""
    facade = MtgCatalogFacade.in_memory()
    facade.import_set_and_cards(
        set_payload_lea(),
        [mono_card_lightning_lea(), bear_card_lea()],
    )
    return facade
