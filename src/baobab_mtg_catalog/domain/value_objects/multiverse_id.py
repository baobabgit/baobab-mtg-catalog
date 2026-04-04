"""Identifiant Multiverse (Gatherer) pour une ressource catalogue historique."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.exceptions.invalid_multiverse_id_error import (
    InvalidMultiverseIdError,
)


@dataclass(frozen=True, slots=True)
class MultiverseId:
    """Entier strictement positif identifiant une carte côté Multiverse / Gatherer.

    :param value: Identifiant numérique.
    :type value: int
    """

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise InvalidMultiverseIdError(
                f"Le multiverse id doit être un entier >= 1 (reçu: {self.value})."
            )

    @classmethod
    def parse(cls, raw: str | int) -> MultiverseId:
        """Construit un multiverse id depuis un entier ou une chaîne décimale.

        :param raw: Valeur entière ou représentation décimale sans espaces.
        :type raw: str | int
        :returns: Identifiant validé.
        :rtype: MultiverseId
        :raises InvalidMultiverseIdError: Si la valeur n'est pas un entier positif.
        """
        if isinstance(raw, int):
            return cls(raw)
        text = raw.strip()
        if not text or not text.isdigit():
            raise InvalidMultiverseIdError(f"Multiverse id non numérique: {raw!r}.")
        return cls(int(text, 10))

    def to_primitive(self) -> int:
        """Représentation primitive pour sérialisation JSON numérique.

        :returns: Entier Gatherer.
        :rtype: int
        """
        return self.value
