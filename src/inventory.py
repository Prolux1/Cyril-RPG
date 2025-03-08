from src.items import Item


class Inventory:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.items = [[None for _ in range(self.rows)] for _ in range(self.cols)]

    def __getitem__(self, index):
        i = index // self.cols
        j = index % self.cols
        return self.items[i][j]

    def __setitem__(self, index, new_item):
        """
        >>> inv = Inventory(12, 12)
        >>> inv[0] = Item("Iron ingot", "Ingot", "15", "Uncommon")
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

    def __contains__(self, item: Item):
        """
        >>> inv = Inventory(12, 12)
        >>> I = Item("Iron ingot", "Ingot", "15", "Uncommon")
        >>> I in inv
        False
        >>> inv.add(I)
        >>> I in inv
        True
        """
        return any(i.name == item.name for i in self if i is not None)

    def add(self, item: Item):
        """
        Add the item in parameters to the list of items
        in this inventory. Replace the first None found.
        :param item:
        :return:
        """
        empty_spot_found = False
        i = 0
        while not empty_spot_found and i < len(self):
            if self[i] is None:
                empty_spot_found = True
                self[i] = item
            i += 1

    def is_full(self):
        return not any(o is None for o in self)












