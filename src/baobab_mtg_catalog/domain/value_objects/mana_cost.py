"""Coût de mana textuel (notation avec accolades), indépendant du fournisseur."""

from __future__ import annotations

import re
from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_mana_cost_error import InvalidManaCostError

_MANA_COST_PATTERN: re.Pattern[str] = re.compile(r"^(\{[^}]+\})*$")
_MAX_LENGTH: int = 256


@dataclass(frozen=True, slots=True)
class ManaCost:
    """Coût de mana sous forme concaténée de symboles ``{...}``.

    Une chaîne vide représente l'absence de coût de mana (ex.: terrains). La
    validation est syntaxique : elle garantit des accolades équilibrées par
    symbole et l'absence de bruit évident, sans simuler toutes les règles de
    parsing Oracle.

    :param value: Séquence de symboles ``{...}`` concaténés.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if len(normalized) > _MAX_LENGTH:
            raise InvalidManaCostError(
                f"Le coût de mana dépasse la longueur maximale ({_MAX_LENGTH})."
            )
        if not _MANA_COST_PATTERN.fullmatch(normalized):
            raise InvalidManaCostError(
                f"Le coût de mana n'est pas une suite valide de symboles {{...}}: "
                f"{self.value!r}."
            )
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, raw: str) -> ManaCost:
        """Construit un coût de mana à partir d'une entrée textuelle.

        :param raw: Texte potentiellement entouré d'espaces.
        :type raw: str
        :returns: Coût validé.
        :rtype: ManaCost
        :raises InvalidManaCostError: Si la syntaxe globale est invalide.
        """
        return cls(raw)

    @classmethod
    def empty(cls) -> ManaCost:
        """Absence de coût de mana."""
        return cls("")

    def is_empty(self) -> bool:
        """Indique si le coût est vide."""
        return self.value == ""

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: Chaîne du coût de mana.
        :rtype: str
        """
        return self.value
