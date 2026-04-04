"""Modèle de domaine du catalogue (cartes, printings, sets, value objects).

Les types sont réexportés depuis ``card_definitions``, ``sets`` et
``value_objects`` : ``from baobab_mtg_catalog.domain import CardDefinition``, etc.
"""

# pylint: disable=unused-wildcard-import,wildcard-import
from baobab_mtg_catalog.domain.card_definitions import *  # noqa: F403
from baobab_mtg_catalog.domain.sets import *  # noqa: F403
from baobab_mtg_catalog.domain.value_objects import *  # noqa: F403
from baobab_mtg_catalog.domain.card_definitions import __all__ as _CD_ALL
from baobab_mtg_catalog.domain.sets import __all__ as _SETS_ALL
from baobab_mtg_catalog.domain.value_objects import __all__ as _VO_ALL

__all__ = list(_CD_ALL) + list(_SETS_ALL) + list(_VO_ALL)
