"""URIs d'illustration associées à un printing (aperçus numériques)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_catalog.domain.card_printings.validation_utils import (
    validate_optional_http_uri,
)
from baobab_mtg_catalog.exceptions.invalid_card_printing_error import (
    InvalidCardPrintingError,
)


@dataclass(frozen=True, slots=True)
class PrintingImageUris:
    """Liens vers les rendus image usuels d'une carte imprimée.

    Tous les champs sont optionnels, mais au moins une URI non vide doit être
    fournie : un agrégat entièrement vide n'apporte aucune information.

    :param small: Aperçu réduit.
    :type small: str | None
    :param normal: Aperçu taille standard.
    :type normal: str | None
    :param large: Aperçu haute résolution.
    :type large: str | None
    :param png: Variante PNG si disponible.
    :type png: str | None
    :param art_crop: Recadrage illustration.
    :type art_crop: str | None
    :param border_crop: Recadrage avec bordure.
    :type border_crop: str | None
    """

    small: str | None = None
    normal: str | None = None
    large: str | None = None
    png: str | None = None
    art_crop: str | None = None
    border_crop: str | None = None

    def __post_init__(self) -> None:
        exc_cls = InvalidCardPrintingError
        small = validate_optional_http_uri(self.small, label="L'URI small", exc_cls=exc_cls)
        normal = validate_optional_http_uri(self.normal, label="L'URI normal", exc_cls=exc_cls)
        large = validate_optional_http_uri(self.large, label="L'URI large", exc_cls=exc_cls)
        png = validate_optional_http_uri(self.png, label="L'URI png", exc_cls=exc_cls)
        art_crop = validate_optional_http_uri(
            self.art_crop, label="L'URI art_crop", exc_cls=exc_cls
        )
        border_crop = validate_optional_http_uri(
            self.border_crop, label="L'URI border_crop", exc_cls=exc_cls
        )
        if not any((small, normal, large, png, art_crop, border_crop)):
            raise InvalidCardPrintingError(
                "PrintingImageUris requiert au moins une URI http(s) non vide."
            )
        object.__setattr__(self, "small", small)
        object.__setattr__(self, "normal", normal)
        object.__setattr__(self, "large", large)
        object.__setattr__(self, "png", png)
        object.__setattr__(self, "art_crop", art_crop)
        object.__setattr__(self, "border_crop", border_crop)
