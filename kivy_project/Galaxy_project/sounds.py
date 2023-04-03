"""
In this file we ghandle everything about the songs in the game
"""

from kivy.core.audio import SoundLoader


def init_audio(self):
    "Methode pour initialiser les differentes musicques ou composantes audio du jeu"
    self.sound_begin = SoundLoader.load("audio/begin.wav")
    self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
    self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
    self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
    self.sound_music1 = SoundLoader.load("audio/music1.wav")
    self.sound_restart = SoundLoader.load("audio/restart.wav")

    self.sound_begin.volume = 0.25
    self.sound_galaxy.volume = 0.25
    self.sound_gameover_impact.volume = 0.45
    self.sound_gameover_voice.volume = 0.75
    self.sound_music1.volume = 1
    self.sound_restart.volume = 0.25
