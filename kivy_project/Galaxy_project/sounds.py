"""
In this file we ghandle everything about the songs in the game
"""

from kivy.core.audio import SoundLoader
from kivy.app import App


def init_audio(self):
    "Methode pour initialiser les differentes musicques ou composantes audio du jeu"
    self.sound_begin = SoundLoader.load("audio/begin.wav")
    self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
    self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
    self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
    self.sound_music1 = SoundLoader.load("audio/music1.wav")
    self.sound_restart = SoundLoader.load("audio/restart.wav")

    # self.sound_begin.volume = (
    #    App.get_running_app().store.get("Sound Volume")["value"] / 100
    # )
    self.sound_galaxy.volume = (
        App.get_running_app().store.get("Sound Volume")["value"] / 100
    )
    # self.sound_gameover_impact.volume = (
    #    App.get_running_app().store.get("SFX Volume")["value"] / 100
    # )
    # self.sound_gameover_voice.volume = (
    #    App.get_running_app().store.get("SFX Volume")["value"] / 100
    # )
    # self.sound_music1.volume = (
    #    App.get_running_app().store.get("Music Volume")["value"] / 100
    # )
    # self.sound_restart.volume = (
    #    App.get_running_app().store.get("Sound Volume")["value"] / 100
    # )
