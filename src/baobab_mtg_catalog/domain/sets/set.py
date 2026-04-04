"""Entité domaine représentant une extension / édition Magic catalogue."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from baobab_mtg_catalog.domain.sets.set_id import SetId
from baobab_mtg_catalog.domain.sets.set_type import SetType
from baobab_mtg_catalog.domain.value_objects.scryfall_id import ScryfallId
from baobab_mtg_catalog.domain.value_objects.set_code import SetCode
from baobab_mtg_catalog.exceptions.invalid_set_error import InvalidSetError

_MAX_NAME_LEN: int = 500
_CONTROL_CHARS: re.Pattern[str] = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_EARLIEST_RELEASE_YEAR: int = 1993
_LATEST_RELEASE_YEAR: int = 2100


@dataclass(frozen=True, slots=True)
class Set:
    """Extension Magic dans le référentiel métier local.

    **Identité d'entité** : deux instances sont considérées égales si elles
    partagent le même :class:`SetId`. Cela reflète la persistance métier.

    **Idempotence d'import** : la clé naturelle de fusion / déduplication
    entre sources externes et référentiel est le :class:`SetCode` (code
    Wizards), exposée via :meth:`natural_key`. Les services d'import devront
    résoudre un set existant sur cette clé (et optionnellement
    ``scryfall_set_id``) avant d'attribuer ou de conserver un ``SetId``.

    Aucune logique d'accès réseau, de persistance ou de requête n'est incluse :
    le modèle est purement domaine.

    :param set_id: Identifiant métier stable (UUID).
    :type set_id: SetId
    :param code: Code d'extension normalisé.
    :type code: SetCode
    :param name: Nom d'affichage du set.
    :type name: str
    :param release_date: Date de sortie officielle (jour).
    :type release_date: date
    :param set_type: Classification du produit extension.
    :type set_type: SetType
    :param card_count: Nombre de cartes annoncé dans le set, si connu.
    :type card_count: int | None
    :param digital_only: Produit réservé au jeu digital.
    :type digital_only: bool
    :param foil_only: Cartes exclusivement en version foil.
    :type foil_only: bool
    :param scryfall_set_id: Identifiant Scryfall du set, pour corrélation import.
    :type scryfall_set_id: ScryfallId | None
    :param parent_set_code: Code du set parent (sous-ensembles, promos liées).
    :type parent_set_code: SetCode | None
    :param block_code: Code de bloc regroupant plusieurs extensions.
    :type block_code: SetCode | None
    """

    set_id: SetId
    code: SetCode
    name: str
    release_date: date
    set_type: SetType
    card_count: int | None = None
    digital_only: bool = False
    foil_only: bool = False
    scryfall_set_id: ScryfallId | None = None
    parent_set_code: SetCode | None = None
    block_code: SetCode | None = None

    def __post_init__(self) -> None:
        normalized_name = self.name.strip()
        if not normalized_name:
            raise InvalidSetError("Le nom du set ne peut pas être vide.")
        if len(normalized_name) > _MAX_NAME_LEN:
            raise InvalidSetError(
                f"Le nom du set dépasse {_MAX_NAME_LEN} caractères: {self.name!r}."
            )
        if _CONTROL_CHARS.search(normalized_name):
            raise InvalidSetError("Le nom du set contient des caractères de contrôle.")
        if self.card_count is not None and self.card_count < 0:
            raise InvalidSetError(
                f"Le nombre de cartes ne peut pas être négatif (reçu: {self.card_count})."
            )
        year = self.release_date.year
        if year < _EARLIEST_RELEASE_YEAR or year > _LATEST_RELEASE_YEAR:
            raise InvalidSetError(
                f"La date de sortie est hors plausibilité ({year}): "
                f"{self.release_date.isoformat()}."
            )
        object.__setattr__(self, "name", normalized_name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Set):
            return NotImplemented
        return self.set_id == other.set_id

    def __hash__(self) -> int:
        return hash(self.set_id)

    def natural_key(self) -> SetCode:
        """Clé naturelle pour aligner un import sur un set déjà connu.

        :returns: Code d'extension Wizards.
        :rtype: SetCode
        """
        return self.code

    def same_extension_as(self, other: Set) -> bool:
        """Indique si deux sets désignent la même extension (même code).

        :param other: Autre entité set.
        :type other: Set
        :returns: Vrai si les codes d'extension sont identiques.
        :rtype: bool
        """
        return self.code == other.code
