"a monster module"
# pylint: disable= attribute-defined-outside-init
import random
import pygame
import animation


class Monster(animation.AnimateSprite):
    "a class that defines the basics of a monster object for the Falling Comet game"
    # initialiser la classe
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 80
        self.max_health = 80
        self.attack = 0.05 + random.random()
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.loot_amount = 10

    def set_loot_amount(self, amount):
        "defining an amount to loot from a monster"
        self.loot_amount = amount

    def set_speed(self, speed):
        "definir une vitesse"
        self.default_speed = speed
        self.velocity = random.randint(0, 2) + random.random()

    def damage(self, amount):
        "damage method"
        self.health -= amount

        # verifier si sa self.health est <= 0 ...
        if self.health <= 0:
            # Supprimer le monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.health = self.max_health
            self.velocity = random.randint(0, self.default_speed) + random.random()
            # ajouter le nombre de points
            self.game.add_score(self.loot_amount)

        # verifier si la barre d'evenement est charge a son max
        if self.game.comet_event.is_full_loading():
            # retirer le/les monstres du jeu
            self.game.all_monsters.remove(self)
            # lancer les cometes
            self.game.comet_event.attempt_fall()

    def update_animation(self) -> None:
        "update the animation"
        self.animate(loop=True)

    def update_health_bar(self, surface):
        "the health bar of a monster"
        # dessiner la barre d'arriere plan
        pygame.draw.rect(
            surface,
            (28, 28, 25),
            [self.rect.x + 20, self.rect.y - 10, self.max_health, 5],
        )
        # dessiner notre barre d'etat
        pygame.draw.rect(
            surface,
            (111, 210, 46),
            [self.rect.x + 20, self.rect.y - 10, self.health, 5],
        )

    def forward(self):
        "moving the monster"
        # peut se deplacer seulement si le monstre n'est pas en colliksin avec un joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            # infliger des degats au Joueur
            self.game.player.damage(self.attack)


# definir une classe pour la momie
class Mummy(Monster):
    "a monster derived class"

    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.size = (130, 130)
        self.set_speed(2)
        self.set_loot_amount(100)


# definir une classe pour l'alien
class Alien(Monster):
    "a monster derived class"

    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 130)
        self.health = 250
        self.max_health = 250
        self.size = (300, 300)
        self.attack = 5
        self.set_speed(1)
        self.set_loot_amount(20)
