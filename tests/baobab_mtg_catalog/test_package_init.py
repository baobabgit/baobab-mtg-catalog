"""Tests du module racine ``baobab_mtg_catalog``."""

import importlib
import importlib.metadata
from unittest.mock import patch

import baobab_mtg_catalog


class TestPackageInit:
    """Vérifie l'API publique et la résolution de version."""

    def test_version_is_non_empty_string(self) -> None:
        """``__version__`` est une chaîne non vide."""
        assert isinstance(baobab_mtg_catalog.__version__, str)
        assert len(baobab_mtg_catalog.__version__) > 0

    def test_public_exports(self) -> None:
        """Les symboles publics incluent l'exception et la version."""
        assert "BaobabMtgCatalogException" in baobab_mtg_catalog.__all__
        assert "__version__" in baobab_mtg_catalog.__all__

    def test_version_fallback_when_not_installed(self) -> None:
        """Repli développeur lorsque les métadonnées du package sont absentes."""
        with patch(
            "importlib.metadata.version",
            side_effect=importlib.metadata.PackageNotFoundError,
        ):
            importlib.reload(baobab_mtg_catalog)
            assert baobab_mtg_catalog.__version__ == "0.1.0"
        importlib.reload(baobab_mtg_catalog)
