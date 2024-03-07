






class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)
