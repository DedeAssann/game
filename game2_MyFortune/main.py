"""
 _summary_

On va essayer d'apprendre certaines choses ici. Donc on se lance a l'aventure sans savoir
vraiment ce qu'on va trouver. On va essayer avec le module kivy.

 _extended_summary_
"""

# pylint: disable= import-error, unused-import, no-member, useless-super-delegation

from my_fortune import fortune
from random import randint
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# Make Sure This Is Always the last import
from kivy import Config

kivy.require("1.9.0")

Config.set('graphics', 'multisamples', '0')

class MyRoot(BoxLayout):
    """
    Cette classe sera la pour generer les nombres generer au hasard.
    """
    
    def __init__(self):
        """
        Methode __init__.
        """
        super(MyRoot, self).__init__()
        
    def generate_number(self):
        "Une methode pour generer des nombres au hasard"
        self.random_label.text = str(randint(0, 1000))
        fortune()

class NeuralRandom(App):
    """
    Cette classe sera la pour gerer l'ecran de notre jeu.
    """

    def build(self):
        """une fonction qui lance un ecran de base"""
        return MyRoot()


if __name__ == "__main__":
    NeuralRandom().run()

