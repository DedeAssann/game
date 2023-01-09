"In this module we initialize the menu"

from kivy.app import App
from kivy.uix.screenmanager import Screen

# from kivy.lang import Builder

# kv = Builder.load_file("menu.kv")


class MenuWidget(Screen):
    "the menu class"

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)


class MenuApp(App):
    "the main class"

    def build(self):
        "a building method"
        return kv


MenuApp().run()
