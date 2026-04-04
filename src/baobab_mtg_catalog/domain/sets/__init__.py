"""Modèles métier des extensions Magic (:class:`Set`)."""

from baobab_mtg_catalog.domain.sets.set import Set
from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.sets.set_type import SetType

__all__: list[str] = ["Set", "SetId", "SetType"]
