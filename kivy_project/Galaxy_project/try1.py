"..."


# configuring the screen which is gonna be open
import os

# os.environ["KCFG_GRAPHICS_FULLSCREEN"] = "auto"

from kivy.config import Config, ConfigParser

# Config.set("graphics", "width", "1200")
# Config.set("graphics", "height", "650")
# Config.set("graphics", "resizable", "1")


# importing the necessary modules
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.settings import Settings
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder

file = Builder.load_file("try1.kv")
config = ConfigParser()
config.read("myconfig.ini")

# settings = Settings()
# settings.add_json_panel("My Panel", config, "file.json")
# __all__ = [""]


class MyApp(App):
    "Yon klas pou eseye sa map aprann nan kivy la a!"

    def build(self):
        return file

    # def build_config(self, config):
    #    Config.setdefaults("graphics", {"width": 1200, "height": 650})

    # def build_settings(self, settings):
    #    jsondata = "file.json"
    #    settings.add_json_panel("Test App", self.config, data=jsondata)


#
# def open_settings(self):
#    return True


# class MyWidget(Widget):
#    "..."
#    pass
#
#
# class MyFirstScreen(Screen):
#    "..."
#    pass


MyApp().run()
