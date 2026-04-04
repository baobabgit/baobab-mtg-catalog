"""Tests de la hiérarchie d'exceptions de validation du domaine."""

import pytest

from baobab_mtg_catalog.exceptions import (
    BaobabMtgCatalogException,
    InvalidColorError,
    InvalidDomainValueError,
)


class TestDomainValidationErrors:
    """Vérifie l'héritage et la levée des erreurs métier."""

    def test_invalid_domain_value_extends_root(self) -> None:
        """``InvalidDomainValueError`` est une erreur catalogue."""
        assert issubclass(InvalidDomainValueError, BaobabMtgCatalogException)

    def test_specific_error_extends_domain_base(self) -> None:
        """Les erreurs fines héritent de la base domaine."""
        assert issubclass(InvalidColorError, InvalidDomainValueError)

    def test_message_on_raise(self) -> None:
        """Le message est conservé sur l'exception levée."""
        with pytest.raises(InvalidColorError) as ctx:
            raise InvalidColorError("bad")
        assert ctx.value.message == "bad"
