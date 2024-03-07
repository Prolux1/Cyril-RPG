import pygame.mixer
import config

pygame.mixer.init()




# Sons du jeu
SON_EQUIPER_ARMURE_LOURDE = pygame.mixer.Sound("./music/inventory/chainmail1.wav")
MUSIC_MENU = pygame.mixer.Sound("./music/music_menu_TOTHETOP.mp3")
MUSIC_ZONE1 = pygame.mixer.Sound("./music/arukas_bloom.mp3")

SONS_ATTAQUE_PERSO = [
    pygame.mixer.Sound(f"./music/battle/sword-unsheathe{i}.wav") for i in range(1, 6)
]

SON_LEVEL_UP = pygame.mixer.Sound("./music/personnage/level_up.mp3")
MUSIC_BOSS = pygame.mixer.Sound("./music/battle/music_boss.wav")

SON_EQUIPER_ARMURE_LOURDE.set_volume(config.SOUND_VOLUME)
MUSIC_MENU.set_volume(config.SOUND_VOLUME)
MUSIC_ZONE1.set_volume(config.SOUND_VOLUME)
SON_LEVEL_UP.set_volume(config.SOUND_VOLUME)
MUSIC_BOSS.set_volume(config.SOUND_VOLUME)
for m in SONS_ATTAQUE_PERSO:
    m.set_volume(config.SOUND_VOLUME)





