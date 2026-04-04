"""Package public API for ``baobab_mtg_catalog``.

Expose la version du distribution package, l'exception racine du projet et la
façade catalogue de haut niveau. L'API détaillée par couche (domaine,
repositories, adaptateurs, services) est documentée dans le README du projet.
"""

from importlib.metadata import PackageNotFoundError, version

from baobab_mtg_catalog.exceptions import BaobabMtgCatalogException
from baobab_mtg_catalog.facades import MtgCatalogFacade

__all__: list[str] = ["BaobabMtgCatalogException", "MtgCatalogFacade", "__version__"]

try:
    __version__: str = version("baobab-mtg-catalog")
except PackageNotFoundError:
    __version__ = "0.1.0"
