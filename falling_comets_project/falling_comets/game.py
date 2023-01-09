"Game module"
# pylint: disable=wildcard-import, no-member, unnecessary-dunder-call
from sounds import SoundManager
from monster import Alien, Mummy
import pygame
from player import Player
from commet_event import CometFallEvent

pygame.init()


# creer une seconde classe qui va representer notre jeu
class Game:
    "a class that implements the basics of the self for self project"

    def __init__(self):
        "initialize the self"
        # definir si le jeu a commencer ou non
        self.is_playing = False
        # generer notre joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # generer levenement
        self.comet_event = CometFallEvent(self)
        # groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        # gerer le son
        self.sound_manager = SoundManager()
        # mettre le score a 0
        self.font = pygame.font.SysFont("Verdania", 36)
        self.score = 0
        self.pressed = {}

    def start(self):
        "start method for the game"
        self.spawn_monsters(Mummy)
        self.spawn_monsters(Mummy)
        self.spawn_monsters(Alien)

    def add_score(self, nbre_points=10):
        "add score to the player score"
        self.score += nbre_points

    def game_over(self):
        """remettre le jeu a neuf, retirer les monstres,
        remettre le joueur a 100 points de vie,
        et mettre le jeu en attente"""
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.all_comets = pygame.sprite.Group()
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        # jouer le son
        self.sound_manager.play("game_over")

    def update(self, screen):
        """update method of the screen
        Li pemet ou pase de yon ecran d'acceuil a ecran jwet la
        """
        # afficher le score sur lecran
        score_text = self.font.render(f"Player SCORE : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        # appliquer l'image de mon joueur sur la fenetre du jeu
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre d'etat du joueur sur l'ecran
        self.player.update_health_bar(screen)

        # actualiser la barre d'evenement du jeu
        self.comet_event.update_bar(screen)

        # actualiser l'animation du joueur
        self.player.update_animation()

        # recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()
        # recuperer les monstres de notre jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        # recuperer les cometes de notre jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        # appliquer l'ensemble des images de mon groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # appliquer l'ensemble des images de mon goupe de monstre
        self.all_monsters.draw(screen)

        # appliquqer l'ensemble des images de mon groupe de cometes
        self.comet_event.all_comets.draw(screen)

        # verifier si le joueur souhaite aller a gauche ou a droite

        if (
            self.pressed.get(pygame.K_RIGHT)
            and self.player.rect.x + self.player.rect.width < screen.get_width()
        ):
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        "check if there's collision between monsters and player"
        return pygame.sprite.spritecollide(
            sprite, group, False, pygame.sprite.collide_mask
        )

    def spawn_monsters(self, monster_class_name):
        "simple method that creates a monster in the self"
        self.all_monsters.add(monster_class_name.__call__(self))
