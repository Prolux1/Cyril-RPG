


class Monde:

    def __init__(self, perso):
        self.pos = 0
        self.zones = []

    def ajouter_zone(self, zone):
        """
        Ajoute une zone au monde
        """
        self.zones.append(zone)
