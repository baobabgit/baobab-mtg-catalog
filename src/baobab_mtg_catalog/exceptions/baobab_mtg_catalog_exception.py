"""Exception racine pour toutes les erreurs métier du catalogue MTG."""


class BaobabMtgCatalogException(Exception):
    """Erreur de base pour tout comportement anormal du package.

    Toutes les exceptions personnalisées du projet doivent hériter de cette
    classe afin de permettre une interception homogène côté consommateurs.

    :param message: Description humaine de l'erreur.
    :type message: str
    """

    def __init__(self, message: str) -> None:
        """Construit l'exception avec un message explicite.

        :param message: Description humaine de l'erreur.
        """
        super().__init__(message)
        self.message: str = message
