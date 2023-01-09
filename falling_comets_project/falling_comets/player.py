"player module"
# pylint: disable=no-member
import pygame
from projectile import Projectile
import animation


pygame.init()

# creer une premiere classe qui va representer notre joueur
class Player(animation.AnimateSprite):
    """a class that defines the basics of a Player for
    the main module of the "Falling Comet" game"""

    def __init__(self, game):
        "to initialize the player"

        super().__init__("player")
        self.game = game
        self.health = 200
        self.max_health = 200
        self.attack = 20
        self.size = (200, 200)
        self.velocity = 3
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def update_animation(self):
        "update the animation"
        self.animate()

    def damage(self, amount):
        "damage method"
        if self.game.check_collision(self, self.game.all_monsters):
            self.health -= amount
        if self.game.check_collision(self, self.game.comet_event.all_comets):
            self.health -= amount
        if self.health <= 0:
            # si le joueur n'as plud de points de vie
            self.game.game_over()

    def update_health_bar(self, surface):
        "the health bar of a monster"
        # dessiner la barre d'arriere plan
        pygame.draw.rect(
            surface,
            (28, 28, 25),
            [20, 50, self.max_health * 5, 20],
        )
        # dessiner notre barre d'etat
        pygame.draw.rect(
            surface,
            (111, 210, 46),
            [20, 50, self.health * 5, 20],
        )

    def launch_projectile(self):
        "creer une nouvelle projectile"
        # demarer l'animation
        self.start_animation()
        self.all_projectiles.add(Projectile(self, self.game))
        # jouer le son
        self.game.sound_manager.play("tir")

    def move_right(self):
        "method for a player object to move it right"
        # si le joueur n'est pas en collision avec un monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        "method for a player object that helps  to move it left"
        self.rect.x -= self.velocity
