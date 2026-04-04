"""Résultat agrégé d'un import set + cartes."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.sets.set import Set


@dataclass(frozen=True, slots=True)
class CatalogImportBatchResult:
    """Statistiques minimales après un import lot ``import_set_and_cards``.

    :param set_obj: Extension telle qu'upsertée dans le référentiel.
    :type set_obj: Set
    :param cards_imported: Nombre de payloads carte traités (une impression par payload).
    :type cards_imported: int
    """

    set_obj: Set
    cards_imported: int
