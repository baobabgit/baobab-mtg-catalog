"""Identifiant Oracle (carte logique) sous forme d'UUID stable."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.value_objects.uuid_canon import canonize_uuid_string
from baobab_mtg_catalog.exceptions.invalid_oracle_id_error import InvalidOracleIdError


@dataclass(frozen=True, slots=True)
class OracleId:
    """UUID représentant l'oracle id (carte logique indépendante du printing).

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
                exc_cls=InvalidOracleIdError,
                invalid_message=f"Oracle id UUID invalide: {self.value!r}.",
            ),
        )

    @classmethod
    def parse(cls, raw: str) -> OracleId:
        """Construit un oracle id à partir d'une entrée textuelle.

        :param raw: UUID sous forme string.
        :type raw: str
        :returns: Identifiant normalisé.
        :rtype: OracleId
        :raises InvalidOracleIdError: Si l'UUID est invalide.
        """
        return cls(raw)

    def to_primitive(self) -> str:
        """Représentation primitive pour sérialisation.

        :returns: UUID en minuscules avec tirets.
        :rtype: str
        """
        return self.value
