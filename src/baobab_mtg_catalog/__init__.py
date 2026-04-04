"""Package public API for ``baobab_mtg_catalog``.

Expose la version du distribution package et l'exception racine du projet.
"""

from importlib.metadata import PackageNotFoundError, version

from baobab_mtg_catalog.exceptions import BaobabMtgCatalogException

__all__: list[str] = ["BaobabMtgCatalogException", "__version__"]

try:
    __version__: str = version("baobab-mtg-catalog")
except PackageNotFoundError:
    __version__ = "0.1.0"
