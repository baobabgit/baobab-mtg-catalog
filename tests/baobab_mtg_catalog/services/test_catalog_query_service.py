"""Tests pour :class:`CatalogQueryService` et les filtres catalogue."""

from __future__ import annotations

import pytest

from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.multiverse_id import MultiverseId
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import SetNotFoundError
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_definition_repository import (
    InMemoryCardDefinitionRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_printing_repository import (
    InMemoryCardPrintingRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_set_repository import (
    InMemorySetRepository,
)
from baobab_mtg_catalog.services import (
    CatalogDefinitionFilter,
    CatalogImportService,
    CatalogPrintingFilter,
    CatalogQueryService,
    CatalogSetFilter,
)

from .scryfall_json_fixtures import bear_card_lea, mono_card_lightning_lea, set_payload_lea


def _stack_with_catalog() -> tuple[CatalogQueryService, CatalogImportService]:
    sets = InMemorySetRepository()
    definitions = InMemoryCardDefinitionRepository()
    printings = InMemoryCardPrintingRepository()
    imp = CatalogImportService(
        set_repository=sets,
        definition_repository=definitions,
        printing_repository=printings,
    )
    imp.import_set_and_cards(
        set_payload_lea(),
        [mono_card_lightning_lea(), bear_card_lea()],
    )
    q = CatalogQueryService(
        set_repository=sets,
        definition_repository=definitions,
        printing_repository=printings,
    )
    return q, imp


class TestCatalogQuerySets:
    """Filtres sur les extensions."""

    def test_find_sets_by_name_substring(self) -> None:
        """Recherche par fragment de nom."""
        q, _ = _stack_with_catalog()
        got = q.find_sets(CatalogSetFilter(name_contains="limited"))
        assert len(got) == 1
        assert got[0].code.value == "LEA"

    def test_find_sets_by_code(self) -> None:
        """Filtre par code exact."""
        q, _ = _stack_with_catalog()
        got = q.find_sets(CatalogSetFilter(set_code=SetCode.parse("lea")))
        assert len(got) == 1


class TestCatalogQueryDefinitions:
    """Filtres sur les définitions."""

    def test_find_definitions_by_name_fragment(self) -> None:
        """Nom normalisé contient la sous-chaîne."""
        q, _ = _stack_with_catalog()
        got = q.find_definitions(
            CatalogDefinitionFilter(normalized_name_contains="bolt"),
        )
        assert len(got) == 1
        assert "Lightning" in got[0].name

    def test_find_definitions_by_oracle_and_color(self) -> None:
        """Combinaison oracle id et couleur."""
        q, _ = _stack_with_catalog()
        oid = OracleId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
        got = q.find_definitions(
            CatalogDefinitionFilter(
                oracle_id=oid,
                any_of_colors=frozenset({Color.GREEN}),
            )
        )
        assert len(got) == 1

    def test_find_definitions_type_line(self) -> None:
        """Filtre sur la ligne de types."""
        q, _ = _stack_with_catalog()
        got = q.find_definitions(CatalogDefinitionFilter(type_line_contains="creature"))
        assert len(got) == 1
        assert "Bear" in got[0].name

    def test_color_identity_within(self) -> None:
        """Cartes jouables dans une identité de deck élargie."""
        q, _ = _stack_with_catalog()
        deck = ColorIdentity.from_iterable([Color.RED, Color.GREEN])
        got = q.find_definitions(CatalogDefinitionFilter(color_identity_within=deck))
        assert len(got) == 2

    def test_empty_filter_lists_all_definitions(self) -> None:
        """Filtre vide : toutes les définitions, ordre stable."""
        q, _ = _stack_with_catalog()
        got = q.find_definitions(CatalogDefinitionFilter())
        assert len(got) == 2
        keys = [d.card_definition_id.value for d in got]
        assert keys == sorted(keys)

    def test_scryfall_card_id_on_definition(self) -> None:
        """Filtre par id Scryfall carte côté définition."""
        q, _ = _stack_with_catalog()
        sid = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        got = q.find_definitions(CatalogDefinitionFilter(scryfall_card_id=sid))
        assert len(got) == 1
        assert "Lightning" in got[0].name


class TestCatalogQueryPrintings:
    """Filtres sur les impressions et critères combinés."""

    def test_find_printings_by_set_code_and_rarity(self) -> None:
        """Set + rareté."""
        q, _ = _stack_with_catalog()
        got = q.find_printings(
            CatalogPrintingFilter(
                set_code=SetCode.parse("lea"),
                rarities=frozenset({Rarity.COMMON}),
            )
        )
        assert len(got) == 2

    def test_find_printings_collector_and_definition(self) -> None:
        """Numéro de collection + sous-filtre définition (couleur)."""
        q, _ = _stack_with_catalog()
        got = q.find_printings(
            CatalogPrintingFilter(
                set_code=SetCode.parse("lea"),
                collector_number=CollectorNumber.parse("116"),
                definition=CatalogDefinitionFilter(
                    any_of_colors=frozenset({Color.RED}),
                ),
            )
        )
        assert len(got) == 1

    def test_find_printings_scryfall_id(self) -> None:
        """Id Scryfall printing."""
        q, _ = _stack_with_catalog()
        sid = ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd")
        got = q.find_printings(CatalogPrintingFilter(scryfall_printing_id=sid))
        assert len(got) == 1

    def test_find_printings_by_card_printing_id(self) -> None:
        """Recherche directe par identifiant métier printing."""
        q, _ = _stack_with_catalog()
        bolt = q.find_printings(
            CatalogPrintingFilter(
                scryfall_printing_id=ScryfallId.parse("dddddddd-dddd-4ddd-8ddd-dddddddddddd"),
            )
        )
        pid = bolt[0].card_printing_id
        got = q.find_printings(CatalogPrintingFilter(card_printing_id=pid))
        assert len(got) == 1
        assert got[0].card_printing_id == pid

    def test_find_printings_multiverse_either_side(self) -> None:
        """Multiverse sur printing ou définition."""
        q, _ = _stack_with_catalog()
        got = q.find_printings(CatalogPrintingFilter(multiverse_id=MultiverseId.parse(600)))
        assert len(got) == 1

    def test_set_code_not_found_raises(self) -> None:
        """Code set inconnu : alignement sur le repository."""
        q, _ = _stack_with_catalog()
        with pytest.raises(SetNotFoundError):
            q.find_printings(CatalogPrintingFilter(set_code=SetCode.parse("xyz")))

    def test_conflicting_set_id_and_code_returns_empty(self) -> None:
        """``set_id`` et ``set_code`` contradictoires."""
        sets = InMemorySetRepository()
        definitions = InMemoryCardDefinitionRepository()
        printings = InMemoryCardPrintingRepository()
        imp = CatalogImportService(
            set_repository=sets,
            definition_repository=definitions,
            printing_repository=printings,
        )
        imp.import_set_and_cards(set_payload_lea(), [mono_card_lightning_lea()])
        q = CatalogQueryService(
            set_repository=sets,
            definition_repository=definitions,
            printing_repository=printings,
        )
        got = q.find_printings(
            CatalogPrintingFilter(
                set_code=SetCode.parse("lea"),
                set_id=SetId.parse("99999999-9999-4999-8999-999999999999"),
            )
        )
        assert not got
