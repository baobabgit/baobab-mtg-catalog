"""Identifiant UUID canonique pour une ressource Scryfall (carte / printing)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions.invalid_scryfall_id_error import InvalidScryfallIdError


@dataclass(frozen=True, slots=True)
class ScryfallId:
    """UUID v4 (ou tout UUID accepté par la lib standard) normalisé en minuscules.

    Ce type matérialise un identifiant externe stable côté Scryfall sans
    dépendre de types du client HTTP : seule la forme UUID est validée ici.

    :param value: UUID sous forme de chaîne avec tirets.
    :type value: str
    """

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            canonize_uuid_string(
                self.value,
                exc_cls=InvalidScryfallIdError,
                invalid_message=f"Identifiant Scryfall UUID invalide: {self.value!r}.",
            ),
        )

    @classmethod
    def parse(cls, raw: str) -> ScryfallId:
        """Construit un identifiant à partir d'une entrée textuelle.

        :param raw: UUID sous forme string.
        :type raw: str
        :returns: Identifiant normalisé.
        :rtype: ScryfallId
        :raises InvalidScryfallIdError: Si l'UUID est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: UUID en minuscules avec tirets.
        :rtype: str
        """
        return self.value
