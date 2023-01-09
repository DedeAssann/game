"""
_extended_summary_
"""
# pylint: disable=import-error

import pygame


class SoundManager:
    "Sound manager class"

    def __init__(self) -> None:
        self.sounds = {
            "click": pygame.mixer.Sound(
                "falling_comets/assets/assets/sounds/click.ogg"
            ),
            "game_over": pygame.mixer.Sound(
                "falling_comets/assets/assets/sounds/game_over.ogg"
            ),
            "meteorite": pygame.mixer.Sound(
                "falling_comets/assets/assets/sounds/meteorite.ogg"
            ),
            "tir": pygame.mixer.Sound("falling_comets/assets/assets/sounds/tir.ogg"),
        }

    def play(self, name):
        "playing sound during the game"
        self.sounds[name].play()
