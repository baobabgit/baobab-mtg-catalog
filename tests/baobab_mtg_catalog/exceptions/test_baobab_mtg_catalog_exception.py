"""Tests pour ``BaobabMtgCatalogException``."""

import pytest

from baobab_mtg_catalog.exceptions.baobab_mtg_catalog_exception import (
    BaobabMtgCatalogException,
)


class TestBaobabMtgCatalogException:
    """Scénarios de base sur l'exception racine."""

    def test_is_exception_subclass(self) -> None:
        """L'exception est une sous-classe standard de ``Exception``."""
        assert issubclass(BaobabMtgCatalogException, Exception)

    def test_message_preserved(self) -> None:
        """Le message est stocké et reflété par ``str()``."""
        message = "erreur catalogue"
        exc = BaobabMtgCatalogException(message)
        assert exc.message == message
        assert str(exc) == message

    def test_can_raise_and_catch(self) -> None:
        """Filtrage homogène via le type projet."""
        with pytest.raises(BaobabMtgCatalogException) as caught:
            raise BaobabMtgCatalogException("boom")
        assert caught.value.message == "boom"
