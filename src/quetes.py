




class Quete:
    def __init__(self, nom: str, description: str, description_rendu: str, objectifs=None, recompenses_items=None, recompenses_moula=None):
        """
        description --> le contexte de la quete
        description_rendu -> le contexte de fin au moment du rendu de la quete (généralement un message de remerciement)
        """
        self.nom = nom
        self.description = description
        self.description_rendu = description_rendu
        self.objectifs = objectifs
        self.recompenses = recompenses_items
        self.recompenses_moula = recompenses_moula













