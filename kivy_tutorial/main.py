"""
_summary_

A simple application

_extended_summary_
"""

# pylint: disable= import-error, unused-import, missing-class-docstring, missing-function-docstring

from cgitb import text
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty()


# the latest import

from kivy import Config


# Window.clearcolor = (1, 1, 1, 1)

Config.set("graphics", "multisamples", "0")


class MyGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def btn(self):
        print("Name:", self.name.text, " | " "email:", self.email.text)
        self.name.text = ""
        self.email.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
