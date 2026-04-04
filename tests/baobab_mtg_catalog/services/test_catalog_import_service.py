"""Tests unitaires et d'intégration interne pour :class:`CatalogImportService`."""

from __future__ import annotations

import pytest

from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_definitions.card_face import CardFace
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.value_objects.card_type_line import CardTypeLine
from baobab_mtg_catalog.domain.value_objects.color import Color
from baobab_mtg_catalog.domain.value_objects.color_identity import ColorIdentity
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.finish import Finish
from baobab_mtg_catalog.domain.value_objects.language import Language
from baobab_mtg_catalog.domain.value_objects.mana_cost import ManaCost
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.rarity import Rarity
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import (
    BaobabMtgCatalogException,
    CatalogImportBatchSetMismatchError,
    CatalogImportInconsistencyError,
    CatalogImportPrintingDefinitionMismatchError,
    CatalogImportSetScryfallMismatchError,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_definition_repository import (
    InMemoryCardDefinitionRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_card_printing_repository import (
    InMemoryCardPrintingRepository,
)
from baobab_mtg_catalog.repositories.in_memory.in_memory_set_repository import (
    InMemorySetRepository,
)
from baobab_mtg_catalog.services.catalog_import_service import CatalogImportService


def _set_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "set",
        "id": "11111111-1111-4111-8111-111111111111",
        "code": "lea",
        "name": "Limited Edition Alpha",
        "set_type": "core",
        "released_at": "1993-08-05",
        "digital": False,
        "foil_only": False,
    }
    base.update(overrides)
    return base


def _mono_card(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "card",
        "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
        "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
        "name": "Lightning Bolt",
        "mana_cost": "{R}",
        "cmc": 1.0,
        "type_line": "Instant",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "colors": ["R"],
        "color_identity": ["R"],
        "lang": "en",
        "rarity": "common",
        "finishes": ["nonfoil"],
        "collector_number": "116",
        "artist": "Christopher Rush",
        "set": "lea",
    }
    base.update(overrides)
    return base


def _second_card(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "object": "card",
        "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "oracle_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "name": "Grizzly Bears",
        "mana_cost": "{1}{G}",
        "cmc": 2.0,
        "type_line": "Creature — Bear",
        "oracle_text": "",
        "colors": ["G"],
        "color_identity": ["G"],
        "lang": "en",
        "rarity": "common",
        "finishes": ["nonfoil"],
        "collector_number": "5",
        "set": "lea",
    }
    base.update(overrides)
    return base


def _stack() -> tuple[
    CatalogImportService,
    InMemorySetRepository,
    InMemoryCardDefinitionRepository,
    InMemoryCardPrintingRepository,
]:
    sets = InMemorySetRepository()
    definitions = InMemoryCardDefinitionRepository()
    printings = InMemoryCardPrintingRepository()
    svc = CatalogImportService(
        set_repository=sets,
        definition_repository=definitions,
        printing_repository=printings,
    )
    return svc, sets, definitions, printings


def _sample_wrong_definition() -> CardDefinition:
    face = CardFace(
        name="Other",
        normalized_name="other",
        mana_cost=ManaCost.parse("{W}"),
        type_line=CardTypeLine.parse("Creature — Other"),
        oracle_text="",
        colors=frozenset({Color.WHITE}),
        power="1",
        toughness="1",
    )
    return CardDefinition(
        card_definition_id=CardDefinitionIdentifier.parse("99999999-9999-4999-8999-999999999999"),
        oracle_id=OracleId.parse("cacacaca-caca-4aca-8aca-cacacacacaca"),
        name=face.name,
        normalized_name=face.normalized_name,
        mana_cost=face.mana_cost,
        mana_value=1.0,
        type_line=face.type_line,
        oracle_text=face.oracle_text,
        colors=face.colors,
        color_identity=ColorIdentity.from_iterable([Color.WHITE]),
        faces=(face,),
        power=face.power,
        toughness=face.toughness,
    )


class TestCatalogImportServiceIntegration:
    """Scénarios bout-en-bout avec repositories in-memory."""

    def test_first_import_nominal(self) -> None:
        """Premier lot : set, deux cartes, relations cohérentes."""
        svc, sets, definitions, printings = _stack()
        sp = _set_payload()
        c1 = _mono_card()
        c2 = _second_card()
        res = svc.import_set_and_cards(sp, [c1, c2])
        assert res.cards_imported == 2
        st = res.set_obj
        assert sets.get_by_code(st.code).set_id == st.set_id
        assert len(definitions.list_all()) == 2
        assert len(printings.list_all()) == 2
        p1 = printings.get_by_scryfall_printing_id(ScryfallId.parse(str(c1["id"])))
        assert p1.set_id == st.set_id
        assert (
            p1.card_definition_id
            == definitions.get_by_oracle_id(OracleId.parse(str(c1["oracle_id"]))).card_definition_id
        )

    def test_reimport_identical_stable_ids(self) -> None:
        """Deuxième passage : mêmes UUID métier pour définitions et printings."""
        svc, _, definitions, printings = _stack()
        sp = _set_payload()
        cards = [_mono_card(), _second_card()]
        svc.import_set_and_cards(sp, cards)
        d_ids_1 = {d.card_definition_id.value for d in definitions.list_all()}
        p_ids_1 = {p.card_printing_id.value for p in printings.list_all()}
        svc.import_set_and_cards(sp, cards)
        d_ids_2 = {d.card_definition_id.value for d in definitions.list_all()}
        p_ids_2 = {p.card_printing_id.value for p in printings.list_all()}
        assert d_ids_1 == d_ids_2
        assert p_ids_1 == p_ids_2

    def test_reimport_partial_update_oracle_payload(self) -> None:
        """Même oracle : nom mis à jour, id définition inchangé."""
        svc, _, definitions, _ = _stack()
        sp = _set_payload()
        c1 = _mono_card()
        svc.import_set_and_cards(sp, [c1])
        oid = OracleId.parse(str(c1["oracle_id"]))
        did_before = definitions.get_by_oracle_id(oid).card_definition_id
        c1_updated = _mono_card(name="Lightning Bolt — errata test")
        svc.import_card(c1_updated, batch_set_code=SetCode.parse("lea"))
        did_after = definitions.get_by_oracle_id(oid).card_definition_id
        assert did_before == did_after
        assert definitions.get_by_oracle_id(oid).name == "Lightning Bolt — errata test"

    def test_set_scryfall_mismatch_on_reimport(self) -> None:
        """Même code set, autre id Scryfall : rejet."""
        svc, _, _, _ = _stack()
        sp = _set_payload()
        svc.import_set(sp)
        sp_bad = {**sp, "id": "22222222-2222-4222-8222-222222222222"}
        with pytest.raises(CatalogImportSetScryfallMismatchError):
            svc.import_set(sp_bad)

    def test_set_reimport_without_scryfall_id_skips_alignment_check(self) -> None:
        """Réimport set sans champ ``id`` : pas d'erreur et ``SetId`` inchangé."""
        svc, sets, _, _ = _stack()
        sp = _set_payload()
        svc.import_set(sp)
        sid1 = sets.get_by_code(SetCode.parse("lea")).set_id
        sp_no_id = {k: v for k, v in sp.items() if k != "id"}
        svc.import_set(sp_no_id)
        sid2 = sets.get_by_code(SetCode.parse("lea")).set_id
        assert sid1 == sid2

    def test_batch_set_field_mismatch(self) -> None:
        """Champ ``set`` de la carte différent du lot."""
        svc, _, _, _ = _stack()
        svc.import_set(_set_payload())
        bad_card = _mono_card(set="mom")
        with pytest.raises(CatalogImportBatchSetMismatchError):
            svc.import_card(bad_card, batch_set_code=SetCode.parse("lea"))

    def test_printing_definition_mismatch_prefixed_state(self) -> None:
        """Printing existant sur l'id Scryfall carte mais mauvaise définition Oracle."""
        svc, sets, definitions, printings = _stack()
        svc.import_set(_set_payload())
        st = sets.get_by_code(SetCode.parse("lea"))
        wrong_def = _sample_wrong_definition()
        definitions.upsert(wrong_def)
        c_payload = _mono_card()
        bad_printing = CardPrinting(
            card_printing_id=CardPrintingIdentifier.parse("77777777-7777-4777-8777-777777777777"),
            card_definition_id=wrong_def.card_definition_id,
            set_id=st.set_id,
            collector_number=CollectorNumber.parse(str(c_payload["collector_number"])),
            language=Language.EN,
            rarity=Rarity.COMMON,
            finishes=frozenset({Finish.NONFOIL}),
            scryfall_printing_id=ScryfallId.parse(str(c_payload["id"])),
        )
        printings.upsert(bad_printing)
        with pytest.raises(CatalogImportPrintingDefinitionMismatchError):
            svc.import_card(c_payload, batch_set_code=SetCode.parse("lea"))

    def test_idempotent_without_scryfall_card_id(self) -> None:
        """Repli sur clé locale ``(set, collector, langue)`` sans ``id`` carte."""
        svc, _, _, printings = _stack()
        sp = _set_payload()
        c = _mono_card()
        del c["id"]
        svc.import_set_and_cards(sp, [c])
        pid1 = printings.list_all()[0].card_printing_id.value
        svc.import_set_and_cards(sp, [dict(c)])
        pid2 = printings.list_all()[0].card_printing_id.value
        assert pid1 == pid2

    def test_printing_set_id_mismatch_after_tamper(self) -> None:
        """Même id Scryfall carte mais printing stocké sur un autre set métier."""
        svc, sets, _, printings = _stack()
        svc.import_set(_set_payload())
        sp_mom = _set_payload(
            code="mom",
            id="33333333-3333-4333-8333-333333333333",
            name="March of the Machine",
        )
        svc.import_set(sp_mom)
        c1 = _mono_card()
        svc.import_card(c1, batch_set_code=SetCode.parse("lea"))
        prev = printings.get_by_scryfall_printing_id(ScryfallId.parse(str(c1["id"])))
        mom = sets.get_by_code(SetCode.parse("MOM"))
        tampered = CardPrinting(
            card_printing_id=prev.card_printing_id,
            card_definition_id=prev.card_definition_id,
            set_id=mom.set_id,
            collector_number=prev.collector_number,
            language=prev.language,
            rarity=prev.rarity,
            finishes=prev.finishes,
            artist=prev.artist,
            image_uris=prev.image_uris,
            released_at=prev.released_at,
            scryfall_printing_id=prev.scryfall_printing_id,
            multiverse_id=prev.multiverse_id,
        )
        printings.upsert(tampered)
        with pytest.raises(CatalogImportPrintingDefinitionMismatchError):
            svc.import_card(c1, batch_set_code=SetCode.parse("lea"))


class TestCatalogImportInheritance:
    """Hiérarchie d'exceptions d'import."""

    def test_inconsistency_base(self) -> None:
        """Les erreurs métier d'import héritent de la base catalogue."""
        assert issubclass(CatalogImportSetScryfallMismatchError, CatalogImportInconsistencyError)
        assert issubclass(CatalogImportSetScryfallMismatchError, BaobabMtgCatalogException)
