




class Quete:
    def __init__(self, nom: str, description: str, description_intermediaire: str = "Vous avez du pain sur la planche !",
                 description_rendu: str = "Vous avez dépassé mes attentes !", objectifs=None, recompenses_items=None, recompenses_moula=None):
        """
            - description --> la description de la quête avant de l'accepter
            - description_intermediaire --> la description de la quête quand elle est en cours c'est ce qui est afficher si
                on retourne parler au Pnj qui nous a donné la quête mais qu'on a pas encore remplit les objectifs pour pouvoir la rendre.
            - description_rendu -> la description au moment du rendu de la quete (ce que nous dit le pnj quand on va rendre la
                quete en ayant remplit tout les objectifs.
        """
        self.nom = nom
        self.description = description
        self.description_intermediaire = description_intermediaire
        self.description_rendu = description_rendu

        self.objectifs = objectifs
        self.recompenses = recompenses_items
        self.recompenses_moula = recompenses_moula













