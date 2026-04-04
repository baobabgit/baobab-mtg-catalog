"""Identifiant métier stable d'une :class:`CardDefinition` dans le référentiel."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions.invalid_card_definition_identifier_error import (
    InvalidCardDefinitionIdentifierError,
)


@dataclass(frozen=True, slots=True)
class CardDefinitionIdentifier:
    """UUID assigné à la définition de carte côté domaine (clé de persistance).

    Distinct de l':class:`~baobab_mtg_catalog.domain.value_objects.oracle_id.OracleId`
    qui sert de clé naturelle métier (même carte logique entre printings).

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
                exc_cls=InvalidCardDefinitionIdentifierError,
                invalid_message=(f"CardDefinitionIdentifier UUID invalide: {self.value!r}."),
            ),
        )

    @classmethod
    def parse(cls, raw: str) -> CardDefinitionIdentifier:
        """Construit un identifiant à partir d'une entrée textuelle.

        :param raw: UUID sous forme string.
        :type raw: str
        :returns: Identifiant normalisé.
        :rtype: CardDefinitionIdentifier
        :raises InvalidCardDefinitionIdentifierError: Si l'UUID est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: UUID en minuscules avec tirets.
        :rtype: str
        """
        return self.value
