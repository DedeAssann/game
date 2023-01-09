"main game module"
# pylint: disable=wildcard-import, no-member, unused-import, import-error

import pygame

from player import Player
from game import Game

pygame.init()

# definir une clock
clock = pygame.time.Clock()
FPS = 80

# generer la fenetre de notre jeu
pygame.display.set_caption("Falling Comets")
screen = pygame.display.set_mode((1280, 738))

# importer/charger l'arriere plan
background = pygame.image.load("falling_comets/assets/assets/bg.jpg")

# charger la baniere
banner = pygame.image.load("falling_comets/assets/assets/banner.png")
# charger notre blouton pour lancer la partie
play_button = pygame.image.load("falling_comets/assets/assets/button.png")
play_button = pygame.transform.scale(play_button, (400, 200))
play_button_rect = play_button.get_rect()
play_button_rect.x = 460
play_button_rect.y = 550


# charger notre jeu
game = Game()

# charger notre joueur
player = Player(game)

RUNNING = True

# boucle tant que la variable RUNNING sera vraie, autrement dit,
# tant que le jeu sera en cours
while RUNNING:

    # appliquer l'arriere-plan
    screen.blit(background, (0, -200))

    # verifier si notre jeu a commence
    if game.is_playing:

        # declencher les instructions de la partie
        game.update(screen)

        # verifier si le jeu n'as pas commence
        # et enclencher l'ecran de bienvenue

    else:
        # appliquer le bouton de lancement du jeu
        screen.blit(play_button, (460, 550))
        # appliquer la baniere
        screen.blit(banner, (250, -80))

    # mettre a jour l'ecran
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():

        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            RUNNING = False
            pygame.quit()
            print("Quit Game")
        # detecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # detecter si la touche espace est enclenchee pour lancer notre projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    # mettre le jeu en mode lancer
                    game.is_playing = True
                    game.start()
                    # jouer le son en question
                    game.sound_manager.play("click")

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verifier si on a cliquer sur le bouton
            if play_button_rect.collidepoint(event.pos):
                # mettre le jeu en mode lancer
                game.is_playing = True
                game.start()
                # jouer le son en question
                game.sound_manager.play("click")

    # fixer le nombre de fps sur ma clock

    clock.tick(FPS)
