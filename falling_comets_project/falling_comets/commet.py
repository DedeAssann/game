"commet manager module"
import random
import pygame
from player import Player

# creer une classe qui gere les cometes
class Comet(pygame.sprite.Sprite):
    "comet class"

    def __init__(self, comet_event):
        "initiating the class"
        super().__init__()
        # definir l'image associee a cette comete
        self.image = pygame.image.load("falling_comets/assets/assets/comet.png")
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 5)
        self.rect.x = random.randint(20, 1300)
        self.rect.y = -random.randint(0, 800)
        self.comet_event = comet_event
        self.player = Player(self.comet_event.game)

    def remove(self):
        "removing comet method"
        self.comet_event.all_comets.remove(self)
        # jouer le son
        self.comet_event.game.sound_manager.play("meteorite")

        # verifier si le nombre de comete sur l'ecran est 0
        if len(self.comet_event.all_comets) == 0:
            # remettre la barre a 0
            self.comet_event.reset_percent()
            # v faire reapparaitre les deux premiers monstres
            self.comet_event.game.start()

    def fall(self):
        "falling comets method"
        self.rect.y += self.velocity

        # ne tombe pas sur le sol
        if self.rect.y >= 500:
            # retirer la boule de feu
            self.remove()
            # si il n'ya plus de boule de feu sur le jeu
            if len(self.comet_event.all_comets) == 0:
                # remettre la jauge au depart
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False

        # verifier s'il y en a plus sur l'ecran
        if len(self.comet_event.all_comets):
            # remettre la jauge au depart
            self.comet_event.reset_percent()
            self.comet_event.fall_mode = False

        # verifier si la boule de feu touche le sol
        if self.comet_event.game.check_collision(
            self, self.comet_event.game.all_players
        ):
            print("Joueur touche!")
            # subir des degats
            self.comet_event.game.player.damage(100)
            # retirer la boule de feu
            self.remove()
