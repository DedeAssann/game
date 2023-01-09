" definir la classe qui va gerer le projectile de notre joueur"

import pygame


class Projectile(pygame.sprite.Sprite):
    "class Projectile for Falling Comets game"

    # definir le constructeur de cette classe
    def __init__(self, player, game):
        super().__init__()
        self.velocity = 25
        self.player = player
        self.game = game
        self.image = pygame.image.load("falling_comets/assets/assets/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 130
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        "methode pour faire tourner le projectile"
        self.angle += 15
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        "eliminer le projectile quand il sort de l'ecran"
        self.player.all_projectiles.remove(self)

    def move(self):
        "deplacer un projectile"
        self.rect.x += self.velocity
        self.rotate()

        # verifier si le projectile entre en collision avec un monstre
        for monster in pygame.sprite.spritecollide(
            self, self.player.game.all_monsters, False, pygame.sprite.collide_mask
        ):
            # supprimer le projectile
            self.remove()
            # infliger des degats aux monstres
            monster.damage(self.player.attack)

        # verifier si notre projectile n'est plus present sur l'ecran
        if self.rect.x > 1360:
            # supprimer le projectile
            self.remove()
