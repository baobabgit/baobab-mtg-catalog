"""Finition de surface d'une impression (non-foil, foil, etc.)."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_finish_error import InvalidFinishError


class Finish(StrEnum):
    """Finition disponible pour un printing dans le modèle catalogue.

    :cvar NONFOIL: Non foil.
    :cvar FOIL: Foil standard.
    :cvar ETCHED: Foil etched (notamment certaines commanders).
    :cvar GLOSSY: Finition glossy promotionnelle.
    :cvar METALPRINT: Estampe métal / traitement spécialisé.
    """

    NONFOIL = "nonfoil"
    FOIL = "foil"
    ETCHED = "etched"
    GLOSSY = "glossy"
    METALPRINT = "metalprint"

    @classmethod
    def parse(cls, raw: str) -> Finish:
        """Interprète une finition fournie sous forme de chaîne normalisée.

        :param raw: Identifiant de finition (ex: ``\"foil\"``).
        :type raw: str
        :returns: Finition reconnue.
        :rtype: Finish
        :raises InvalidFinishError: Si la finition n'est pas supportée.
        """
        value = raw.strip().lower()
        if not value:
            raise InvalidFinishError("La finition ne peut pas être vide.")
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidFinishError(f"Finition inconnue: {raw!r}.") from exc
