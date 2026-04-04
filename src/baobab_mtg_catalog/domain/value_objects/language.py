"""Langue d'impression ou de texte de carte dans le référentiel catalogue."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_language_error import InvalidLanguageError


class Language(StrEnum):
    """Code de langue stable utilisé pour les printings catalogue.

    Les valeurs suivent les codes usuels du domaine MTG / internationalisation.
    Elles ne dépendent pas d'un schéma JSON fournisseur : tout adaptateur doit
    mapper vers ces codes.

    :cvar EN: Anglais.
    :cvar FR: Français.
    :cvar ES: Espagnol.
    :cvar DE: Allemand.
    :cvar IT: Italien.
    :cvar PT: Portugais.
    :cvar JA: Japonais.
    :cvar KO: Coréen.
    :cvar RU: Russe.
    :cvar ZHS: Chinois simplifié.
    :cvar ZHT: Chinois traditionnel.
    :cvar HE: Hébreu.
    :cvar LA: Latin.
    :cvar GRC: Grec ancien.
    :cvar AR: Arabe.
    :cvar SA: Sanskrit.
    :cvar PHYREXIAN: Phyrexian.
    """

    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    JA = "ja"
    KO = "ko"
    RU = "ru"
    ZHS = "zhs"
    ZHT = "zht"
    HE = "he"
    LA = "la"
    GRC = "grc"
    AR = "ar"
    SA = "sa"
    PHYREXIAN = "phyrexian"

    @classmethod
    def parse(cls, raw: str) -> Language:
        """Parse un code de langue normalisé en minuscules.

        :param raw: Code langue (ex: ``\"fr\"``, ``\"zhs\"``).
        :type raw: str
        :returns: Langue connue du domaine.
        :rtype: Language
        :raises InvalidLanguageError: Si le code n'est pas supporté.
        """
        code = raw.strip().lower()
        if not code:
            raise InvalidLanguageError("Le code de langue ne peut pas être vide.")
        try:
            return cls(code)
        except ValueError as exc:
            raise InvalidLanguageError(f"Code de langue inconnu: {raw!r}.") from exc
