


from src import pnjs




class Quete:
    def __init__(self, nom: str, description: str, description_intermediaire: str,
                 description_rendu: str, objectifs=None, recompenses_items=None, recompenses_moula=None):
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

    def peut_etre_terminee(self) -> bool:
        return False



class QueteTuerPnjs(Quete):
    def __init__(self, nom: str, description: str, pnjs_a_tuers: list[tuple[type[pnjs.Pnj], int]], description_intermediaire: str = "Vous avez du pain sur la planche !",
                 description_rendu: str = "Vous avez dépassé mes attentes !"):
        """
        Le paramètre "liste_pnjs_a_tuers" est une liste de tuples dans lesquelles il est indiqué en 1er
        le type du pnj à tuer et en deuxième la quantité à tuer (donc > 0), ce qui permet d'avoir une quete
        regroupant plusieurs objectifs comme tuer 5 rats mais aussi tuer 1 boss rat (c'est absolument succulent).
        """
        super().__init__(nom, description, description_intermediaire, description_rendu)

        self.pnjs_a_tuers = pnjs_a_tuers

        # Contient à l'emplacement i la quantité du ième pnj de "self.pnjs_a_tuers" tué
        self.pnjs_tuers = [0] * len(pnjs_a_tuers)

    def peut_etre_terminee(self) -> bool:
        for i in range(len(self.pnjs_a_tuers)):
            if self.pnjs_tuers[i] < self.pnjs_a_tuers[i][1]: # normalement on ne dépasse pas le nombre fixé de pnjs à tuer mais on sait jamais
                return False
        return True







