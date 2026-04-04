"""Identifiant métier stable d'un ``Set`` dans le référentiel catalogue."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions.invalid_set_id_error import InvalidSetIdError


@dataclass(frozen=True, slots=True)
class SetId:
    """UUID assigné au set côté domaine (clé de persistance / égalité d'entité).

    Ce n'est pas l'identifiant Scryfall : il est généré ou attribué par
    l'application lors de la première intégration du set. Les réimports
    idempotents s'appuient en complément sur le :class:`SetCode` (clé naturelle).

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
                exc_cls=InvalidSetIdError,
                invalid_message=f"SetId UUID invalide: {self.value!r}.",
            ),
        )

    @classmethod
    def parse(cls, raw: str) -> SetId:
        """Construit un ``SetId`` à partir d'une entrée textuelle.

        :param raw: UUID sous forme string.
        :type raw: str
        :returns: Identifiant normalisé.
        :rtype: SetId
        :raises InvalidSetIdError: Si l'UUID est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: UUID en minuscules avec tirets.
        :rtype: str
        """
        return self.value
