from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

# @kv = Builder.load_file("try.kv")


class TryApp(App):
    "..."


class SecondWindow(Screen):
    display_text = StringProperty("Hiii !")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_button_pressed(self, letter: str):
        self.display_text = letter


class MainWindow(Screen):
    background_image = ObjectProperty(Image(source="bg1.jpg", anim_delay=1))


TryApp().run()
