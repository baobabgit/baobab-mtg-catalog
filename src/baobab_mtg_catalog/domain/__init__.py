"""Modèle de domaine du catalogue (cartes, printings, sets, value objects).

Les types partagés sont réexportés depuis ``value_objects`` et ``sets`` :
``from baobab_mtg_catalog.domain import Color, Set``, etc.
"""

# pylint: disable=unused-wildcard-import,wildcard-import
from baobab_mtg_catalog.domain.sets import *  # noqa: F403
from baobab_mtg_catalog.domain.value_objects import *  # noqa: F403
from baobab_mtg_catalog.domain.sets import __all__ as _SETS_ALL
from baobab_mtg_catalog.domain.value_objects import __all__ as _VO_ALL

__all__ = list(_VO_ALL) + list(_SETS_ALL)
