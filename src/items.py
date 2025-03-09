

class Item:
    def __init__(self, nom, item_type, lvl, rarity, icon_name):
        self.nom = nom
        self.type = item_type
        self.lvl = lvl
        self.rarity = rarity

        self.icon_name = icon_name


class Equipment(Item):
    def __init__(self, nom, equipment_type, lvl, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(nom, equipment_type, lvl, rarity, icon_name)
        self.bonus_hp = bonus_hp
        self.bonus_strength = bonus_strength


class Armor(Equipment):
    def __init__(self, nom, armor_type, lvl, armor, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(nom, armor_type, lvl, bonus_hp, bonus_strength, rarity, icon_name)
        self.armor = armor


class Weapon(Equipment):
    def __init__(self, nom, weapon_type, lvl, damage, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(nom, weapon_type, lvl, bonus_hp, bonus_strength, rarity, icon_name)
        self.damage = damage



















