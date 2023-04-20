"""
My Settings Module
"""

# pylint: disable= no-name-in-module, unused-import, wrong-import-position
from kivy.core.window import Window

Window.allow_screen_saver = True

import cProfile
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    StringProperty,
    Clock,
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.storage.jsonstore import JsonStore
import re


btn1 = Button(
    text="60 fps",
    size_hint_y=None,
    height=50,
    font_name="fonts/Lcd.ttf",
    font_size="30dp",
)
btn2 = Button(
    text="80 fps",
    size_hint_y=None,
    height=50,
    font_name="fonts/Lcd.ttf",
    font_size="30dp",
)
btn3 = Button(
    text="80 fps",
    size_hint_y=None,
    height=50,
    font_name="fonts/Lcd.ttf",
    font_size="30dp",
)


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


class Infos(Popup):
    "..."

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        self.size_hint = (0.825, 0.825)
        self.input_name.text = App.get_running_app().store.get("Name of User")["value"]
        self.input_age.text = App.get_running_app().store.get("Age of User")["value"]
        self.input_mail.text = App.get_running_app().store.get("Mail of User")["value"]

    def w_infos(self):
        "Write infos in the storage file about the user name"
        App.get_running_app().store.put(
            "Name of User", name="Name", value=self.input_name.text
        )
        App.get_running_app().store.put(
            "Age of User", name="Age", value=self.input_age.text
        )
        App.get_running_app().store.put(
            "Mail of User", name="Mail", value=self.input_mail.text
        )

    def on_submit(self):
        "..."
        if self.lbl1.opacity == 1:
            pass
        else:
            self.w_infos()
            self.input_name.opacity = 0
            self.input_age.opacity = 0
            self.input_mail.opacity = 0
            self.lbl1.text = App.get_running_app().store.get("Name of User")["value"]
            self.lbl2.text = App.get_running_app().store.get("Age of User")["value"]
            self.lbl3.text = App.get_running_app().store.get("Mail of User")["value"]
            self.lbl1.opacity = 1
            self.lbl2.opacity = 1
            self.lbl3.opacity = 1

    def modify(self):
        if self.input_name.opacity == 1:
            pass
        else:
            self.lbl1.opacity = 0
            self.lbl2.opacity = 0
            self.lbl3.opacity = 0
            self.input_name.opacity = 1
            self.input_age.opacity = 1
            self.input_mail.opacity = 1


class About(Popup):
    "..."

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)


class Connect(Popup):
    "..."

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)


class Score(Popup):
    "..."
    score_nb = None  # 78
    best_score_nb = None  # 150
    reset = False
    score = StringProperty()
    best_score = StringProperty()
    reset_btn = ObjectProperty()

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        self.size_hint = (0.785, 0.785)
        self.reset_at_close = self.on_dismiss()
        self.score_nb = App.get_running_app().store.get("Score")["value"]
        self.best_score_nb = App.get_running_app().store.get("Best Score")["value"]
        self.score = "Y O U R   L A S T   S C O R E : " + str(self.score_nb)
        self.best_score = "B E S T   S C O R E : " + str(self.best_score_nb)

    def on_progress(self):
        "..."
        Clock.schedule_interval(self.reset_score, 1.0 / 60.0)
        Clock.schedule_interval(self.on_dismiss, 1.0 / 60)

    def reset_score(self, _dt=(1.0 / 60)):
        "..."
        if self.reset_btn.state == "down":
            self.reset_at_close = True
            self.reset = True
            App.get_running_app().store.put("Score", name="Score", value=0)
            App.get_running_app().store.put("Best Score", name="Best Score", value=0)
            self.score_nb = App.get_running_app().store.get("Score")["value"]
            self.best_score_nb = App.get_running_app().store.get("Best Score")["value"]
            self.score = "Y O U R   S C O R E : " + str(self.score_nb)
            self.best_score = "B E S T   S C O R E : " + str(self.best_score_nb)

    def on_dismiss(self, *_dt):
        "..."
        if self.disabled is True:
            self.reset_at_close = self.reset
            return self.reset_at_close


class StackWidget(StackLayout):
    "..."
    label_list = []
    n_widget = NumericProperty(12)
    app = ObjectProperty()
    score_nb = None
    best_score_nb = None

    def show_scores(self):
        "..."
        if Score.reset is True:
            Score.open(Score(score_nb=0, best_score_nb=0, reset=False))
        Score.open(Score())

    def show_infos(self):
        "..."
        Infos.open(Infos())

    def show_about(self):
        "..."
        About.open(About())

    def show_connect(self):
        "..."
        Connect.open(Connect())

    def get_fullscreen(self, args: list):
        "..."
        if self.l_1.fullscreen_btn.active is True:
            Window.fullscreen = "auto"
        else:
            Window.fullscreen = 0


class L2(RelativeLayout):
    "..."
    max_fps = App.get_running_app().store.get("Max FPS Level")["value"]
    fps_limit = StringProperty(str(round(max_fps)))

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_progress, 1.0 / 60)

    def on_progress(self, _dt):
        "..."
        self.l2_lbl.text = str(
            int(App.get_running_app().store.get("Max FPS Level")["value"])
        )

    def inc_fps_limit(self, value: str):
        "..."
        if value == "-":
            if self.max_fps <= 40:
                pass
            else:
                self.max_fps -= 10
        elif value == "+":
            if self.max_fps >= 90:
                pass
            else:
                self.max_fps += 10
        else:
            pass
        self.fps_limit = str(self.max_fps)
        App.get_running_app().store.put(
            "Max FPS Level", name="limit FPS", value=round(self.max_fps)
        )

        return self.max_fps, self.fps_limit


class L3(RelativeLayout):
    "..."
    max_fps = App.get_running_app().store.get("Current FPS Level")["value"]
    cur_fps_limit = StringProperty(str(round(max_fps)))
    l3_lbl = ObjectProperty()

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_progress, 1.0 / 60)

    def on_progress(self, _dt):
        widget = self.l_2
        if widget.max_fps <= self.max_fps:
            self.max_fps = widget.max_fps
            App.get_running_app().store.put(
                "Current FPS Level", name="FPS", value=round(self.max_fps)
            )
            self.l3_lbl.text = str(
                int(App.get_running_app().store.get("Current FPS Level")["value"])
            )

    def inc_cur_fps_limit(self, value: str, widget):
        "..."

        if value == "-":
            if self.max_fps <= 40:
                pass
            else:
                self.max_fps -= 10
        elif value == "+":
            if self.max_fps == widget.max_fps or self.max_fps >= 90:
                pass
            else:
                self.max_fps += 10
        else:
            pass
        self.cur_fps_limit = str(self.max_fps)

        App.get_running_app().store.put(
            "Current FPS Level", name="FPS", value=self.max_fps
        )

        return self.max_fps, self.cur_fps_limit


class L8(RelativeLayout):
    "..."
    text_to_display = StringProperty()

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)
        Clock.schedule_interval(self.get_label_text, 1.0 / 60)

    def get_label_text(self, _dt):
        "..."
        text = {
            0: "B e g i n n e r",
            1: "I n t e r m e d i a t e",
            2: "A d v a n c e d",
            3: "E x p e r t",
        }
        self.text_to_display = text[round(self.my_slider.value)]
        App.get_running_app().store.put(
            "Level", name="Level", value=self.my_slider.value
        )


class SettingsWidget(RelativeLayout):
    "..."

    def __init__(self, **kwargs):
        "..."
        super().__init__(**kwargs)