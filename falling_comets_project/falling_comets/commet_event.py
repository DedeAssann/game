"commet event program"

import pygame
from commet import Comet


class CometFallEvent:
    "commet fall class"

    # lors du lancement -> creer un compteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False

        # definir un groupe de sprite pour stocker nos cometes
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        "add percentage method"
        self.percent += self.percent_speed / 100
        return self.percent

    def is_full_loading(self):
        """if_full_loading method"""
        return self.percent >= 100

    def reset_percent(self):
        """reset_percent method"""
        self.percent = 0

    def meteor_fall(self):
        "faire apparaitre une premiere boule de feu"
        for _ in range(10):
            self.all_comets.add(Comet(self))

    def attempt_fall(self):
        """attempt_fall method"""
        if self.is_full_loading() and len(self.game.all_monsters) == 0:
            # 1 lancer la pluie de meteores
            self.meteor_fall()
            # 3
            self.fall_mode = True

    def update_bar(self, surface):
        "the update bar method"
        # incrementer la barre
        self.add_percent()

        # la barre noire en arriere plan
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            [
                0,  # l'axe des x
                surface.get_height() - 20,  # l'axe des y
                surface.get_width(),  # longueur de la fenetre
                10,  # epaisseur de la barre
            ],
        )
        # la barre rouge: compteur de l'evenement
        pygame.draw.rect(
            surface,
            (187, 11, 11),
            [
                0,  # l'axe des x
                surface.get_height() - 20,  # l'axe des y
                (surface.get_width() / 100) * self.percent,  # longueur de la fenetre
                10,  # epaisseur de la barre
            ],
        )
