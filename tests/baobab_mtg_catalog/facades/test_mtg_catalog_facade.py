"""Tests d'intégration de :class:`MtgCatalogFacade`."""

from __future__ import annotations

from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.services import CatalogDefinitionFilter, CatalogPrintingFilter

from tests.baobab_mtg_catalog.services.scryfall_json_fixtures import set_payload_lea


class TestMtgCatalogFacadeInMemory:
    """Fabrique et câblage."""

    def test_in_memory_starts_empty(self) -> None:
        """Les repositories sont vides avant import."""
        facade = MtgCatalogFacade.in_memory()
        assert facade.sets.list_all() == ()

    def test_import_set_and_cards_delegates_to_importer(
        self, lea_catalog_facade: MtgCatalogFacade
    ) -> None:
        """Après import, le set est résolu par code."""
        st = lea_catalog_facade.sets.get_by_code(SetCode.parse("lea"))
        assert st.name == "Limited Edition Alpha"

    def test_importer_property_and_shortcut_import(self) -> None:
        """La propriété ``importer`` et le raccourci renvoient le même résultat."""
        facade = MtgCatalogFacade.in_memory()
        payload = set_payload_lea()
        via_prop = facade.importer.import_set_and_cards(payload, [])
        via_short = facade.import_set_and_cards(payload, [])
        assert via_prop.set_obj.set_id == via_short.set_obj.set_id
        assert via_prop.cards_imported == via_short.cards_imported == 0


class TestMtgCatalogFacadeUseCases:
    """Cas d'usage transverses via la façade."""

    def test_get_definition_by_oracle_and_name_contains(
        self,
        lea_catalog_facade: MtgCatalogFacade,
    ) -> None:
        """Carte logique par oracle id et par fragment de nom."""
        f = lea_catalog_facade
        by_oracle = f.definitions.get_by_oracle_id(
            OracleId.parse("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"),
        )
        assert by_oracle.normalized_name == "lightning bolt"
        found = f.definitions.find_by_name_contains("grizzly")
        assert len(found) == 1
        assert found[0].normalized_name == "grizzly bears"

    def test_get_printing_by_scryfall_and_list_for_definition(
        self,
        lea_catalog_facade: MtgCatalogFacade,
    ) -> None:
        """Printing par id Scryfall et liste par définition."""
        f = lea_catalog_facade
        scry = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        p = f.printings.get_by_scryfall_printing_id(scry)
        defs = f.definitions.get_by_id(p.card_definition_id)
        again = f.printings.list_for_definition(defs.card_definition_id)
        assert len(again) == 1
        assert again[0].scryfall_printing_id == scry

    def test_list_printings_for_set_and_filter_in_set(
        self,
        lea_catalog_facade: MtgCatalogFacade,
    ) -> None:
        """Printings du set et filtre rareté commune dans l'extension."""
        f = lea_catalog_facade
        st = f.sets.get_by_code(SetCode.parse("lea"))
        all_p = f.printings.list_for_set(st.set_id)
        assert len(all_p) == 2
        commons = f.printings.find_in_set(
            st.set_id,
            CatalogPrintingFilter(rarities=frozenset({Rarity.COMMON})),
        )
        assert len(commons) == 2

    def test_catalog_advanced_filter(self, lea_catalog_facade: MtgCatalogFacade) -> None:
        """Accès direct au service de filtres combinés."""
        f = lea_catalog_facade
        got = f.catalog.find_definitions(
            CatalogDefinitionFilter(normalized_name_contains="bolt"),
        )
        assert len(got) == 1
