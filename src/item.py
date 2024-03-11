

class Item:
    def __init__(self, name, item_type, lvl, rarity, icon_name):
        self.name = name
        self.type = item_type
        self.lvl = lvl
        self.rarity = rarity

        self.icon_name = icon_name


class Equipment(Item):
    def __init__(self, name, equipment_type, lvl, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(name, equipment_type, lvl, rarity, icon_name)
        self.bonus_hp = bonus_hp
        self.bonus_strength = bonus_strength


class Armor(Equipment):
    def __init__(self, name, armor_type, lvl, armor, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(name, armor_type, lvl, bonus_hp, bonus_strength, rarity, icon_name)
        self.armor = armor


class Weapon(Equipment):
    def __init__(self, name, weapon_type, lvl, damage, bonus_hp, bonus_strength, rarity, icon_name):
        super().__init__(name, weapon_type, lvl, bonus_hp, bonus_strength, rarity, icon_name)
        self.damage = damage



















