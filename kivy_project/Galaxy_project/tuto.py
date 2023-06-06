"This module is responsible for the tutorial of the game, whenever it needs to be displayed"

# pylint: disable= no-name-in-module, wrong-import-position, wrong-import-order

from kivy.app import App
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    Clock,
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rotate
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
import re


# class WindowManagerTuto(ScreenManager):
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        transition = NoTransition(duration=0)
#        self.transition = transition


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


class FirstWidget(RelativeLayout):
    pass


class FirstWindow(Screen):
    "..."
    first_widget = FirstWidget()
    transit_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # translator = TranslatedText()
        self.load_widget = LoadingWidget()
        self.add_widget(self.load_widget)

    def on_pre_enter(self):
        if App.get_running_app().progress_empty() is True:
            self.remove_widget(self.first_widget)
        else:
            self.add_widget(self.first_widget)

    def transit_screen(self):
        self.first_widget.opacity = 0
        self.transit_widget = TransitionWidget()
        self.add_widget(self.transit_widget)

    def switch_screen(self):
        first_widget = FirstWidget()
        if App.get_running_app().progress_empty() is False:
            self.add_widget(first_widget)
        else:
            self.manager.current = "home_screen"

    def save_infos(self):
        infos = {
            "Last Name": self.first_widget.stack.l1.last_name.text,
            "First Name": self.first_widget.stack.l2.first_name.text,
            "Mail of User": self.first_widget.stack.l3.mail.text,
            "Age of User": self.first_widget.stack.l4.age.text,
            "Username": self.first_widget.stack.l6.username.text,
        }
        if infos["Last Name"] != "" or infos["First Name"] != "":
            App.get_running_app().store.put(
                "Name of User",
                name="Name",
                value=infos["Last Name"] + " " + infos["First Name"],
            )
        if infos["Age of User"] != "":
            App.get_running_app().store.put(
                "Age of User", name="Age", value=infos["Age of User"]
            )
        if infos["Mail of User"] != "":
            App.get_running_app().store.put(
                "Mail of User", name="Mail", value=infos["Mail of User"]
            )
        if infos["Username"] != "":
            App.get_running_app().store.put(
                "Username", name="Username", value=infos["Username"]
            )


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
            font_name="fonts/gtr.ttf",
            font_size=dp(80),
            underline=True,
            pos_hint={"center": (0.5, 0.8)},
            size_hint=(0.5, 0.4),
            color=(0.458, 0.866, 0.866, 1),
        )
        self.add_widget(self.label)

    def on_parent(self, widget, parent):
        anim1 = Animation(value=100, duration=0)
        anim2 = Animation(opacity=0, duration=0)
        anim2.bind(on_complete=lambda *args: self.parent.switch_screen())
        anim1.bind(on_complete=lambda *args: anim2.start(self))
        anim1.start(self.progress)


class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = MyCustomDropDown()
        self.mainbutton = Button(
            text="Select...",
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "top": 0.95},
            bold=True,
            font_name="fonts/gtr.ttf",
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


class MainButton(Button):
    pass


class MyCustomDropDown(DropDown):
    global LANGUAGES
    LANGUAGES = {"ENGLISH": "en", "FRANCAIS": "fr", "ESPANOL": "es"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LANGUAGES = LANGUAGES


# The Second Window & it's widgets
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
            on_complete=lambda *args: setattr(
                App.get_running_app().root, "current", "second"
            )
        )
        anim.start(self)


class SecondWidget(RelativeLayout):
    wlcm_text = (
        "\nWelcome to your G a l a x y Journey, \nCaptain {}.\n\n".format("D E D E")
        + "Let's begin with how to guide your starship throughout the GALAXY.\n As we begin, consider agreeing to the User License."
    )

    def on_parent(self, widget, parent):
        anim = Animation(opacity=0, duration=15)
        anim.bind(
            on_complete=lambda *args: setattr(self.parent.third_widget, "opacity", 1.0)
        )
        anim.start(self)


class SyncLabel(Label):
    angle = NumericProperty(0)
    anim = ObjectProperty(None)

    def on_angle(self, instance, angle):
        self.canvas.before.clear()
        with self.canvas.before:
            Rotate(angle=angle, origin=self.center)

    def start_animation(self):
        for _ in range(2):
            self.anim = Animation(angle=360, duration=0)
            self.anim += Animation(size=(600, 100), duration=0)
            self.anim += Animation(
                size=(self.texture_size[0] + dp(10), self.texture_size[1] + dp(5)),
                duration=3,
            )
            self.anim += Animation(size=(600, 100), duration=0)
            self.anim.repeat = True
        self.anim.start(self)


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


class Tutorial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pre_tuto = PreTutorial()
        self.pre_tuto = pre_tuto

    def on_enter(self):
        self.add_widget(self.pre_tuto)


class PreTutorial(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, widget, parent):
        parent.tuto_01.opacity = 0
        anim = Animation(opacity=0, duration=5)
        anim.bind(on_complete=lambda *args: setattr(parent.tuto_01, "opacity", 1.0))
        anim.start(self)


class Tutorial01(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
