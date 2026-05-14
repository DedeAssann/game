"""
_summary_

Ce module est votre module chance de la journee.
Il vous donne le nombre qui vous est attribue pour la journee,
votre roulette qui determine votre niveau de chance durant la journee,
et vous l'exprime par une phrase.

Pour ce faire, ce module appelle le module random, pour avoir acces
a certaines de ses composantes, qu'il va utiliser en vue de generer des
nombres au hasard, et choisir la phrase qui traduit votre chance pour la journee.

_extended_summary_
"""
# pylint: disable= import-error, unused-import, unnecesary-pass
import random as rdm

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import Rotate
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
# Latest import :
from kivy import Config

Window.clearcolor = (1, 1, 1, 1)

kivy.require("1.9.0")

Config.set("graphics", "multisamples", "0")

lucky_quotes = {
    1: "Today is your lucky day",
    2: "Today won't be as you expected it, but it'll be worth it. ",
    3: "You still can choose a brighter path in your life.",
    4: "Today should be a wise day for you",
    5: """Be aware! Love is awaiting you from now on.
    But be careful not to fall of...""",
    6: "Good morning my friend ! ",
    7: "You have choosen a path were you'll have to work. Be smart today!",
    8: "You must think about your life, and the choices you are making.",
}

midday_quotes = {
    "_"
}

afternoon_quotes = {
    "_"
}

before_bed_quotes = {
    "_"
}

morning_quotes = {
    "_"
}

# This part when we handle everything about the application
# and the kivy management

# 1) La se kote nap gerer class ki responsab spinning wheel lan

Builder.load_string("""
<Loading>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
    Image:
        source: "wheel.png"
        size_hint: None, None
        size: 600, 600
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
""")


class Loading(FloatLayout):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2)
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


# 2) la nap eseye jere spinning wheel lan

class Wheel(Widget):
    pass


# 3) la nap jere res app la



class Generator(Widget):
    """
    Cette class s'occupera de gerer la fonction fortune
    """
    wheel = ObjectProperty(None)
    def __init__(self):
        "init method"
        super(Generator, self).__init__()


    def fortune(self):
        "the fortune function"


    def animate(self):
        "the animation method"
        return self.spin_wheel()

    def spin_wheel(self):
        "a spinning wheel method"
        self.wheel.rotate()



class FortuneApp(App):
    """
    Cette classe sera la principale a gerer le fonctionnement de l'application
    """

    def build(self):
        """
        Une fonction qui lance l'ecran de base
        """
        return Generator()



if __name__ == "__main__":
    FortuneApp().run()
