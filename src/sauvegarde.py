from __future__ import annotations

import os
import pickle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg


class Sauvegarde:
    def __init__(self, jeu: CyrilRpg | None):
        if jeu is not None:
            self.joueur = jeu.joueur
        else:
            self.joueur = None


def charger_sauvegarde() -> Sauvegarde:
    """
    All data will be pickle and saved in save/data.pkl.
    """
    save = Sauvegarde(None)
    # We load data only if save directory exists,
    # else we create it
    if os.path.isdir("save"):
        # If the data.pkl file exist, we load the data
        # else we do nothing because we have nothing to load
        if os.path.isfile("save/save.pkl"):
            with open("save/save.pkl", "rb") as save_file:
                save: Sauvegarde = pickle.load(save_file)
    else:
        os.mkdir(os.path.join("save"))
        save = Sauvegarde(None)
    return save


def ecrire_sauvegarde(jeu: CyrilRpg):
    if not os.path.isdir("save"):
        os.mkdir(os.path.join("save"))

    with open("save/save.pkl", "wb") as save_file:
        pickle.dump(Sauvegarde(jeu), save_file)  # The warning "Expected type 'SupportsWrite[bytes]', got 'BinaryIO' instead" is erroneous.


