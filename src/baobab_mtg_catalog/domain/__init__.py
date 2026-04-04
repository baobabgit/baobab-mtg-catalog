"""Modèle de domaine du catalogue (cartes, printings, sets, value objects).

Les types partagés sont réexportés depuis ``value_objects`` : préférer
``from baobab_mtg_catalog.domain import Color``, etc.
"""

# pylint: disable=unused-wildcard-import,wildcard-import
from baobab_mtg_catalog.domain.value_objects import *  # noqa: F403
from baobab_mtg_catalog.domain.value_objects import __all__
