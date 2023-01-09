from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_file("try.kv")


class MyMainApp(App):
    def build(self):
        return kv


MyMainApp().run()
