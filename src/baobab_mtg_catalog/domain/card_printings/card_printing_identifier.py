"""Identifiant métier stable d'un printing dans le référentiel catalogue."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions.invalid_card_printing_identifier_error import (
    InvalidCardPrintingIdentifierError,
)


@dataclass(frozen=True, slots=True)
class CardPrintingIdentifier:
    """UUID assigné au printing côté domaine (clé de persistance / égalité d'entité).

    Distinct des identifiants fournisseurs (``ScryfallId``, etc.) utilisés pour
    l'idempotence d'import (voir ``CardPrinting.natural_key``).

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
                exc_cls=InvalidCardPrintingIdentifierError,
                invalid_message=f"CardPrintingIdentifier UUID invalide: {self.value!r}.",
            ),
        )

    @classmethod
    def parse(cls, raw: str) -> CardPrintingIdentifier:
        """Construit un identifiant à partir d'une entrée textuelle.

        :param raw: UUID sous forme string.
        :type raw: str
        :returns: Identifiant normalisé.
        :rtype: CardPrintingIdentifier
        :raises InvalidCardPrintingIdentifierError: Si l'UUID est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: UUID en minuscules avec tirets.
        :rtype: str
        """
        return self.value
