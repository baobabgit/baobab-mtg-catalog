"""Service d'import idempotent Scryfall → référentiel métier local."""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from typing import Any

from baobab_mtg_catalog.adapters.scryfall.scryfall_card_definition_adapter import (
    ScryfallCardDefinitionAdapter,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_card_printing_adapter import (
    ScryfallCardPrintingAdapter,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_normalize import (
    language_from_scryfall,
    optional_scryfall_id,
)
from baobab_mtg_catalog.adapters.scryfall.scryfall_payload import optional_str, require_str
from baobab_mtg_catalog.adapters.scryfall.scryfall_set_adapter import ScryfallSetAdapter
from baobab_mtg_catalog.domain.card_definitions.card_definition import CardDefinition
from baobab_mtg_catalog.domain.card_definitions.card_definition_identifier import (
    CardDefinitionIdentifier,
)
from baobab_mtg_catalog.domain.card_printings.card_printing import CardPrinting
from baobab_mtg_catalog.domain.card_printings.card_printing_identifier import (
    CardPrintingIdentifier,
)
from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.value_objects.collector_number import CollectorNumber
from baobab_mtg_catalog.domain.value_objects.oracle_id import OracleId
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions import (
    CardDefinitionNotFoundError,
    CardPrintingNotFoundError,
    SetNotFoundError,
)
from baobab_mtg_catalog.exceptions.catalog_import_batch_set_mismatch_error import (
    CatalogImportBatchSetMismatchError,
)
from baobab_mtg_catalog.exceptions.catalog_import_printing_definition_mismatch_error import (
    CatalogImportPrintingDefinitionMismatchError,
)
from baobab_mtg_catalog.exceptions.catalog_import_set_scryfall_mismatch_error import (
    CatalogImportSetScryfallMismatchError,
)
from baobab_mtg_catalog.repositories.card_definition_repository import CardDefinitionRepository
from baobab_mtg_catalog.repositories.card_printing_repository import (
    CardPrintingRepository,
    PrintingNaturalKey,
)
from baobab_mtg_catalog.repositories.set_repository import SetRepository
from baobab_mtg_catalog.services.catalog_import_batch_result import CatalogImportBatchResult


class CatalogImportService:
    """Importe des objets JSON Scryfall déjà représentables en ``Mapping`` (sans réseau).

    **Clés de fusion (matching)**

    - **Set** : :class:`SetCode` issu du champ ``code`` du payload set. Le
      :class:`SetId` est réutilisé si un set existe déjà sous ce code. Si le set
      stocké et le payload portent tous deux un ``id`` Scryfall non nul, ils
      doivent coïncider sinon :class:`CatalogImportSetScryfallMismatchError`.
    - **CardDefinition** : :class:`OracleId` (champ ``oracle_id`` de la carte).
      Le :class:`CardDefinitionIdentifier` métier est réutilisé si l'oracle est
      déjà connu ; sinon un nouvel UUID est attribué. Le contenu Oracle est
      toujours reconstruit via :class:`ScryfallCardDefinitionAdapter` puis
      :meth:`CardDefinitionRepository.upsert` (mise à jour idempotente).
    - **CardPrinting** : si le champ ``id`` (UUID carte Scryfall) est présent,
      fusion sur :class:`~baobab_mtg_catalog.domain.value_objects.scryfall_id.ScryfallId` ;
      sinon triplet ``(set_id métier, collector_number, language)`` aligné sur
      :meth:`CardPrinting.natural_key`. Le :class:`CardPrintingIdentifier` est
      réutilisé si une impression existe pour cette clé.

    **Cohérence**

    - Chaque payload carte doit avoir un champ ``set`` (code) identique au code
      du set du lot (:class:`CatalogImportBatchSetMismatchError` sinon).
    - Un printing existant pour la même clé doit déjà référencer la même
      définition et le même set métier (:class:`CatalogImportPrintingDefinitionMismatchError`).

    :param set_repository: Stockage des extensions.
    :type set_repository: SetRepository
    :param definition_repository: Stockage des définitions Oracle.
    :type definition_repository: CardDefinitionRepository
    :param printing_repository: Stockage des impressions.
    :type printing_repository: CardPrintingRepository
    """

    def __init__(
        self,
        *,
        set_repository: SetRepository,
        definition_repository: CardDefinitionRepository,
        printing_repository: CardPrintingRepository,
    ) -> None:
        """Attache les repositories cibles de l'import."""
        self._sets = set_repository
        self._definitions = definition_repository
        self._printings = printing_repository

    def import_set(self, payload: Mapping[str, Any]) -> Set:
        """Résout le ``SetId`` par ``SetCode`` puis upsert via l'adaptateur set.

        :param payload: Objet JSON Scryfall ``set``.
        :returns: Set enregistré.
        :raises CatalogImportSetScryfallMismatchError: Si l'id Scryfall du set contredit le stock.
        """
        code = SetCode.parse(require_str(payload, "code"))
        try:
            existing = self._sets.get_by_code(code)
            set_id = existing.set_id
            self._ensure_set_scryfall_aligned(existing, payload)
        except SetNotFoundError:
            set_id = SetId.parse(str(uuid.uuid4()))
        entity = ScryfallSetAdapter.to_set(payload, set_id=set_id)
        return self._sets.upsert(entity)

    def import_card(
        self,
        payload: Mapping[str, Any],
        *,
        batch_set_code: SetCode,
    ) -> tuple[CardDefinition, CardPrinting]:
        """Importe une carte : définition Oracle + printing pour le set du lot.

        :param payload: Objet JSON Scryfall ``card``.
        :param batch_set_code: Code du set auquel le lot doit appartenir.
        :returns: Paire définition et impression upsertées.
        :raises CatalogImportBatchSetMismatchError: Si le champ ``set`` de la carte diverge.
        :raises SetNotFoundError: Si aucun set métier n'existe pour ``batch_set_code``.
        :raises CatalogImportPrintingDefinitionMismatchError: Si une clé printing existante
            référence d'autres identifiants métier que ceux résolus pour le payload.
        """
        card_set_code = SetCode.parse(require_str(payload, "set"))
        if card_set_code != batch_set_code:
            raise CatalogImportBatchSetMismatchError(
                f"La carte annonce le set {card_set_code.value!r}, le lot attend "
                f"{batch_set_code.value!r}."
            )
        st = self._sets.get_by_code(batch_set_code)
        oracle_id = OracleId.parse(require_str(payload, "oracle_id"))
        definition_id = self._resolve_definition_id(oracle_id)
        definition = ScryfallCardDefinitionAdapter.to_card_definition(
            payload,
            card_definition_id=definition_id,
        )
        self._definitions.upsert(definition)
        printing_id = self._resolve_printing_id(payload, st, definition.card_definition_id)
        printing = ScryfallCardPrintingAdapter.to_card_printing(
            payload,
            card_printing_id=printing_id,
            card_definition_id=definition.card_definition_id,
            set_id=st.set_id,
        )
        return definition, self._printings.upsert(printing)

    def import_set_and_cards(
        self,
        set_payload: Mapping[str, Any],
        card_payloads: Sequence[Mapping[str, Any]],
    ) -> CatalogImportBatchResult:
        """Enchaîne :meth:`import_set` puis :meth:`import_card` pour chaque carte.

        :param set_payload: JSON Scryfall ``set``.
        :param card_payloads: Séquence de JSON ``card`` du même produit.
        :returns: Résultat avec le set et le nombre de cartes traitées.
        """
        st = self.import_set(set_payload)
        for card_payload in card_payloads:
            self.import_card(card_payload, batch_set_code=st.code)
        return CatalogImportBatchResult(set_obj=st, cards_imported=len(card_payloads))

    def _ensure_set_scryfall_aligned(self, existing: Set, payload: Mapping[str, Any]) -> None:
        incoming = optional_scryfall_id(payload, "id")
        if existing.scryfall_set_id is None or incoming is None:
            return
        if existing.scryfall_set_id.value != incoming.value:
            raise CatalogImportSetScryfallMismatchError(
                f"Le set {existing.code.value!r} est déjà lié au scryfall_set_id "
                f"{existing.scryfall_set_id.value!r}; le payload annonce {incoming.value!r}."
            )

    def _resolve_definition_id(self, oracle_id: OracleId) -> CardDefinitionIdentifier:
        try:
            found = self._definitions.get_by_oracle_id(oracle_id)
            return found.card_definition_id
        except CardDefinitionNotFoundError:
            return CardDefinitionIdentifier.parse(str(uuid.uuid4()))

    def _resolve_printing_id(
        self,
        payload: Mapping[str, Any],
        st: Set,
        definition_id: CardDefinitionIdentifier,
    ) -> CardPrintingIdentifier:
        scry = optional_scryfall_id(payload, "id")
        if scry is not None:
            return self._printing_id_for_scryfall(st, definition_id, scry)
        return self._printing_id_for_local_natural_key(payload, st, definition_id)

    def _printing_id_for_scryfall(
        self,
        st: Set,
        definition_id: CardDefinitionIdentifier,
        scry: ScryfallId,
    ) -> CardPrintingIdentifier:
        try:
            prev = self._printings.get_by_scryfall_printing_id(scry)
        except CardPrintingNotFoundError:
            return CardPrintingIdentifier.parse(str(uuid.uuid4()))
        self._ensure_printing_consistent(prev, definition_id, st.set_id)
        return prev.card_printing_id

    def _printing_id_for_local_natural_key(
        self,
        payload: Mapping[str, Any],
        st: Set,
        definition_id: CardDefinitionIdentifier,
    ) -> CardPrintingIdentifier:
        cn = CollectorNumber.parse(require_str(payload, "collector_number"))
        lang_raw = optional_str(payload, "lang") or "en"
        language = language_from_scryfall(lang_raw)
        key: PrintingNaturalKey = (st.set_id, cn, language)
        try:
            prev = self._printings.get_by_natural_key(key)
        except CardPrintingNotFoundError:
            return CardPrintingIdentifier.parse(str(uuid.uuid4()))
        self._ensure_printing_consistent(prev, definition_id, st.set_id)
        return prev.card_printing_id

    @staticmethod
    def _ensure_printing_consistent(
        existing: CardPrinting,
        definition_id: CardDefinitionIdentifier,
        set_id: SetId,
    ) -> None:
        if existing.card_definition_id != definition_id:
            raise CatalogImportPrintingDefinitionMismatchError(
                "Un printing existe déjà pour cette clé Scryfall (ou locale) mais pointe vers "
                "une autre CardDefinitionIdentifier que celle résolue pour l'oracle_id du payload."
            )
        if existing.set_id != set_id:
            raise CatalogImportPrintingDefinitionMismatchError(
                "Un printing existe déjà pour cette clé mais est rattaché à un autre SetId métier."
            )
