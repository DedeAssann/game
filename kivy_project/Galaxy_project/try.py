from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

# @kv = Builder.load_file("try.kv")


class TryApp(App):
    "..."
    # def build(self):
    #    return kv


class SecondWindow(Screen):
    display_text = StringProperty("Hiii !")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_button_pressed(self, letter: str):
        self.display_text = letter


TryApp().run()
