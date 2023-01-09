"""
Main python module of the calclator project
"""
# pylint: disable = unused-import

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

# the latest import ...
from kivy import Config

# configuration of the app environment
Config.set("graphics", "multisamples", "0")


class MyAppScreen(Widget):
    """
    klas sa ap jere tout sa ki ap paret sou ecran application an
    """


class MyCalculatorApp(App):
    """
    Klas sa se principale klas application an
    """

    def build(self):
        "fonction ki pou lancer application an"
        return MyAppScreen()


if __name__ == "__main__":
    MyCalculatorApp().run()
