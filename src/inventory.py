from src import items


class Inventory:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.items = [[None for _ in range(self.rows)] for _ in range(self.cols)]

    def __getitem__(self, index):
        i = index // self.cols
        j = index % self.cols
        return self.items[i][j]

    def __setitem__(self, index: int, new_item: items.Item | None):
        """
        >>> inv = Inventory(12, 12)
        >>> inv[0] = items.Item("Iron ingot", "Ingot", "15", "Uncommon", "Skibidi Icon")
        """
        i = index // self.cols
        j = index % self.cols
        self.items[i][j] = new_item

    def __len__(self):
        """
        >>> inv = Inventory(12, 12)
        >>> len(inv)
        144
        """
        return self.rows * self.cols

    def __contains__(self, item: items.Item):
        """
        >>> inv = Inventory(12, 12)
        >>> I = items.Item("Iron ingot", "Ingot", "15", "Uncommon", "Skibidi Icon")
        >>> I in inv
        False
        >>> inv.add(I)
        >>> I in inv
        True
        """
        return any(i.nom == item.nom for i in self if i is not None)

    def chercher(self, item: items.Item | None) -> int | None:
        """
        Cherche l'item passé en paramètre dans l'inventaire et renvoie :
            - l'indice de l'item dans l'inventaire s'il est dedans (peut aussi prendre None pour renvoyer la première case vide)
            - None sinon (et pas -1 parceque [-1] chope le dernier élément donc c'est pas fou)
        """
        trouvee = False
        i = 0
        while not trouvee and i < len(self):
            if self[i] == item:
                trouvee = True
            else:
                i += 1

        return i if trouvee else None


    def add(self, item: items.Item):
        """
        Add the item in parameters to the list of items
        in this inventory. Replace the first None found.
        :param item:
        :return:
        """
        indice_case_vide = self.chercher(None)
        if indice_case_vide is not None:
            self[indice_case_vide] = item

    def retirer(self, piece_equipement: items.Equipment):
        """
        Retire l'équipement passé en paramètre de l'inventaire.
        """
        indice_piece_equipement = self.chercher(piece_equipement)
        if indice_piece_equipement is not None:
            self[indice_piece_equipement] = None

    def is_full(self):
        return not any(o is None for o in self)











