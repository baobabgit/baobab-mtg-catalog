"""Classification métier d'une extension Magic (alignement usages catalogue)."""

from __future__ import annotations

from enum import StrEnum

from baobab_mtg_catalog.exceptions.invalid_set_type_error import InvalidSetTypeError


class SetType(StrEnum):
    """Type d'extension tel que couramment distingué dans les données catalogue.

    Les libellés suivent les valeurs usuelles des flux MTG / Scryfall ; tout
    adaptateur doit mapper les sources externes vers ces constantes.

    :cvar ALCHEMY: Ensemble alchemy / rebalance digital.
    :cvar ARCHENEMY: Deck Archenemy.
    :cvar ARSENAL: Arsenal (produits spécialisés).
    :cvar BOX: Produit type box / collection.
    :cvar COMMANDER: Deck commander préconstruit.
    :cvar CORE: Set core / édition de base.
    :cvar DRAFT_INNOVATION: Innovation draft (ex. Jumpstart).
    :cvar DUEL_DECK: Duel Deck.
    :cvar EXPANSION: Extension standard.
    :cvar FROM_THE_VAULT: From the Vault.
    :cvar FUNNY: Cartes humour / académiques hors formats sérieux.
    :cvar MASTERPIECE: Série Masterpiece.
    :cvar MEMORABILIA: Mémorabilia.
    :cvar MINIGAME: Mini-jeu.
    :cvar PLANECHASE: Planechase.
    :cvar PREMIUM_DECK: Premium Deck Series.
    :cvar PROMO: Promo générique.
    :cvar SPELLBOOK: Spellbook.
    :cvar STARTER: Starter / intro.
    :cvar TOKEN: Produits token.
    :cvar TREASURE_CHEST: Treasure Chest (MTGO).
    :cvar VANGUARD: Vanguard.
    """

    ALCHEMY = "alchemy"
    ARCHENEMY = "archenemy"
    ARSENAL = "arsenal"
    BOX = "box"
    COMMANDER = "commander"
    CORE = "core"
    DRAFT_INNOVATION = "draft_innovation"
    DUEL_DECK = "duel_deck"
    EXPANSION = "expansion"
    FROM_THE_VAULT = "from_the_vault"
    FUNNY = "funny"
    MASTERPIECE = "masterpiece"
    MEMORABILIA = "memorabilia"
    MINIGAME = "minigame"
    PLANECHASE = "planechase"
    PREMIUM_DECK = "premium_deck"
    PROMO = "promo"
    SPELLBOOK = "spellbook"
    STARTER = "starter"
    TOKEN = "token"  # nosec B105
    TREASURE_CHEST = "treasure_chest"
    VANGUARD = "vanguard"

    @classmethod
    def parse(cls, raw: str) -> SetType:
        """Interprète une valeur textuelle normalisée en snake_case.

        :param raw: Type de set (ex. expansion, draft_innovation).
        :type raw: str
        :returns: Valeur d'énumération.
        :rtype: SetType
        :raises InvalidSetTypeError: Si la valeur est inconnue.
        """
        value = raw.strip().lower()
        if not value:
            raise InvalidSetTypeError("Le type de set ne peut pas être vide.")
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidSetTypeError(f"Type de set inconnu: {raw!r}.") from exc
