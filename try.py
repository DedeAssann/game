# pylint: disable= no-name-in-module, unused-import, wrong-import-position, wrong-import-order

from kivy.config import Config

Config.set("graphics", "width", "1200")
Config.set("graphics", "height", "650")
Config.set("graphics", "resizable", True)
Config.write()

from kivy.core.window import Window

# from translation import TranslatedText

Window.allow_screensaver = True

from kivy.app import App
import cProfile
from kivy.uix.slider import Slider
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    StringProperty,
    Clock,
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rotate, Color, Rectangle, PopMatrix, PushMatrix
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, NoTransition, ScreenManager
from kivy.storage.jsonstore import JsonStore
import re

store = JsonStore("tryapp.json")

Window.allow_screensaver = True


#
class MyCustomDropDown(DropDown):
    global LANGUAGES
    LANGUAGES = {"E N G L I S H": "en", "F R A N C A I S": "fr", "E S P A N O L": "es"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LANGUAGES = LANGUAGES


#
class MainButton(Button):
    pass


#
class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = MyCustomDropDown()
        self.mainbutton = Button(
            text="Select...",
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "top": 0.95},
            bold=True,
            font_name="kivy_project/Galaxy_project/fonts/Sackers-Gothic-Std-Light.ttf",
            font_size=dp(35),
            background_color=(0, 0, 0, 0),
            color=(0.458, 0.866, 0.866, 1),
        )
        self.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(
            on_select=lambda instance, x: setattr(self.mainbutton, "text", x)
        )

    def callback(self, instance, x):
        print("The chosen mode is: {0}".format(x))


#
class FirstWindow(Screen):
    "..."
    first_widget = ObjectProperty()
    transit_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # translator = TranslatedText()
        self.load_widget = LoadingWidget()
        self.add_widget(self.load_widget)

    def transit_screen(self):
        self.first_widget.opacity = 0
        self.transit_widget = TransitionWidget()
        self.add_widget(self.transit_widget)


#
class SecondWidget(RelativeLayout):
    wlcm_text = (
        "W e l c o m e\n\n".center(1).upper()
        + "t o  y o u r  {}, C a p t a i n  {}.\n\n".format(
            "G a l a x y  J o u r n e y", "D E D E"
        )
        + "L e t ' s  b e g i n  w i t h  h o w  t o  g u i d e  y o u r\n\ns t a r s h i p  t h r o u g h o u t  t h e  G A L A X Y .\n\nA s  w e  b e g i n ,  c o n s i d e r\n\na g r e e i n g  t o  t h e  U s e r  L i c e n s e ."
    )

    def on_parent(self, widget, parent):
        anim = Animation(opacity=0, duration=15)
        anim.bind(
            on_complete=lambda *args: setattr(self.parent.third_widget, "opacity", 1.0)
        )
        anim.start(self)


#
class ThirdWidget(RelativeLayout):
    "..."
    eula_text = """
            End-User License Agreement (EULA) for Galaxy Game\n\nGalaxy Game End-User License Agreement

            PLEASE READ THIS AGREEMENT CAREFULLY BEFORE USING THE GALAXY GAME. \nBY INSTALLING, DOWNLOADING, OR OTHERWISE USING THE GAME, YOU AGREE TO BE BOUND BY THE TERMS OF THIS AGREEMENT. IF YOU DO NOT AGREE TO THE TERMS OF THIS AGREEMENT, DO NOT INSTALL, DOWNLOAD, OR USE THE GAME.

            1. License Grant. Subject to the terms of this Agreement, the developer grants you a non-exclusive, non-transferable, limited license to use the Galaxy Game for your personal, non-commercial use.

            2. Restrictions. You may not modify, copy, distribute, sell, or transfer the Galaxy Game or any part of it without the developer's prior written consent.

            3. Ownership. The Galaxy Game is owned by the developer and is protected by copyright and other intellectual property laws. The developer retains all rights, title, and interest in and to the Galaxy Game.

            4. Disclaimer of Warranties. THE GALAXY GAME IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

            5. Limitation of Liability. TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL THE DEVELOPER BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF BUSINESS PROFITS, BUSINESS INTERRUPTION, LOSS OF BUSINESS INFORMATION, OR ANY OTHER PECUNIARY LOSS) ARISING OUT OF THE USE OF OR INABILITY TO USE THE GALAXY GAME, EVEN IF THE DEVELOPER HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

            6. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the state of California, without regard to its conflicts of law principles.

            7. Termination. This Agreement shall terminate automatically if you fail to comply with any of the terms and conditions of this Agreement. Upon termination, you must immediately cease all use of the Galaxy Game and destroy all copies of the Galaxy Game in your possession.

            8. Miscellaneous. This Agreement constitutes the entire agreement between you and the developer with respect to the Galaxy Game, and supersedes all prior or contemporaneous communications and proposals, whether oral or written, between you and the developer. If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.
        """


#
class SyncLabel(Label):
    angle = NumericProperty(0)
    anim = ObjectProperty(None)

    def on_angle(self, instance, angle):
        self.canvas.before.clear()
        with self.canvas.before:
            Rotate(angle=angle, origin=self.center)

    def start_animation(self):
        for _ in range(2):
            self.anim = Animation(angle=360, duration=3)
            self.anim += Animation(size=(600, 100), duration=3)
            self.anim += Animation(
                size=(self.texture_size[0] + dp(10), self.texture_size[1] + dp(5)),
                duration=3,
            )
            self.anim += Animation(size=(600, 100), duration=3)
            self.anim.repeat = True
        self.anim.start(self)


#
class LoadingWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = ProgressBar(
            max=100,
            value=20,
            pos_hint={"center": (0.5, 0.2)},
            size_hint=(0.4, 0.5),
            width=dp(200),
        )
        self.add_widget(self.progress)
        self.label = Label(
            text="W  E  L  C  O  M  E",
            font_name="kivy_project/Galaxy_project/fonts/Sackers-Gothic-Std-Light.ttf",
            font_size=dp(80),
            underline=True,
            pos_hint={"center": (0.5, 0.8)},
            size_hint=(0.5, 0.4),
            color=(0.458, 0.866, 0.866, 1),
        )
        self.add_widget(self.label)

    def on_parent(self, widget, parent):
        anim = Animation(value=100, duration=10)
        anim.bind(on_complete=lambda *args: setattr(self, "opacity", 0))
        anim.start(self.progress)


#
class TransitionWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sync = SyncLabel()
        self.add_widget(self.sync)
        self.sync.start_animation()

    def on_parent(self, widget, parent):
        Clock.schedule_once(self.animate, 10)

    def animate(self, *args):
        anim = Animation(opacity=0, duration=1)
        anim.bind(
            on_complete=lambda *args: setattr(self.parent.manager, "current", "second")
        )
        anim.start(self)


#
class Tutorial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pre_tuto = PreTutorial()
        self.pre_tuto = pre_tuto

    def on_enter(self):
        self.add_widget(self.pre_tuto)


#
class PreTutorial(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, widget, parent):
        parent.tuto_01.opacity = 0
        anim = Animation(opacity=0, duration=5)
        anim.bind(on_complete=lambda *args: setattr(parent.tuto_01, "opacity", 1.0))
        anim.start(self)


#
class Tutorial01(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


#
class SecondWindow(Screen):
    second_widget = ObjectProperty()
    third_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_screens(self):
        self.second_widget = SecondWidget()
        self.add_widget(self.second_widget)

    def on_enter(self):
        self.add_screens()


#
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        transition = NoTransition(duration=0)
        self.transition = transition


#
class TryApp(App):
    "..."
    use_kivy_settings = False
    title = "|   M y   G a l a x y   S e t t i n g s   D e m o   |"
    store = store

    def translate(self):
        pass

    def on_key_down(self, touch):
        for key in Window.keycodes:
            if key == "escape":
                pass

    def open_settings(self, *largs):
        pass

    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()
        self.store = store

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats("tryapp.profile")

    def on_pause(self):
        return True

    def on_resume(self):
        pass


#
class FloatInput(TextInput):
    "..."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pat = re.compile("[^0-9]")

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if "." in self.text:
            s = re.sub(pat, "", substring)
        else:
            s = ".".join(re.sub(pat, "", s) for s in substring.split(".", 1))
        return super().insert_text(s, from_undo=from_undo)


#
class StringInput(TextInput):
    "..."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    _values = re.compile("[0-9]")

    def insert_text(self, substring, from_undo=False):
        _values = self._values
        if "." in self.text:
            s = re.sub(_values, "", substring)
        else:
            s = ".".join(re.sub(_values, "", s) for s in substring.split(".", 1))
        return super().insert_text(s, from_undo=from_undo)


TryApp().run()


# ***https://www.youtube.com/watch?v=5JOaTtcg1tE&t=18s***
