"""
A project in a virtual environment to learn kivy
Project name : The Lab
"""
# python3.9
# pylint: disable = missing-class-docstring, unused-import, invalid-name, missing-function-docstring, no-name-in-module, pointless-string-statement

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.pagelayout import PageLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.properties import Clock
from kivy.graphics.context_instructions import Color
from kivy import Config

Config.set("graphics", "multisamples", "0")

# 2nd part of the project


class WidgetExample(GridLayout):
    my_text = StringProperty("1")
    count = 1
    count_enabled = BooleanProperty(False)
    # slider_value_txt = StringProperty("50")
    # slide_enabled = BooleanProperty(False)
    my_text_input_txt = StringProperty("Foo!")

    def on_button_click(self):
        print("Button Clicked!")
        if self.count_enabled:
            self.count += 1
            self.my_text = str(self.count)
        else:
            pass

    def on_toggle_button_state(self, widget):
        print("Toggle state!" + widget.state)
        if widget.state == "normal":
            widget.text = "OFF"
            self.count_enabled = False
        else:
            widget.text = "ON"
            self.count_enabled = True

    def on_switch_active(self, widget):
        print("Switch: " + str(widget.active))
        # self.slide_enabled = str(widget.active)

    # def on_slider_value(self, widget):
    # if self.slide_enabled:
    # print("Slider: " + str(int(widget.value)))
    # self.slider_value_txt = str(int(widget.value))

    def on_text_validate(self, widget):
        print("Validate!")
        self.my_text_input_txt = str(widget.text)


# 1st part of the project

# class PageLayoutExample(PageLayout):
#    pass


class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = "lr-tb"
        for _ in range(0, 100):
            b = Button(text=str(_ + 1), size_hint=(None, None), size=(dp(100), dp(100)))
            self.add_widget(b)


# class GridLayoutExample(GridLayout):
#    pass

# class AnchorLayoutExample(AnchorLayout):
#    pass


class BoxLayoutExample(BoxLayout):
    # How to write all the code in the python file
    # def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    #    self.orientation = "vertical"
    #    b1 = Button(text="A")
    #    b2 = Button(text="B")
    #    b3 = Button(text="C")
    #    self.add_widget(b1)
    #    self.add_widget(b2)
    #    self.add_widget(b3)
    pass


# class MainWidget(Widget):
#    pass


class TheLabApp(App):
    pass


class CanvasExample1(Widget):
    pass


class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(dp(100), dp(100), dp(400), dp(500)), width=2)
            Color(0, 1, 0)
            Line(circle=(dp(250), dp(100), dp(80)), width=2)
            Line(rectangle=(dp(300), dp(200), dp(150), dp(100)), width=2)
            self.rect = Rectangle(pos=(500, 200), size=(150, 100))

    def on_button_a_click(self):
        # print("foo")

        x, y = self.rect.pos
        width, _ = self.rect.size
        inc = dp(10)

        diff = self.width - (x + width)
        if diff < inc:
            inc = diff

        x += inc
        self.rect.pos = (x, y)


class CanvasExample5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        self.vx = dp(4)
        self.vy = dp(2)
        with self.canvas:
            self.ball = Ellipse(pos=self.center, size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update, 1 / 60)

    def on_size(self, *args):
        print("on size: " + str(self.width) + "," + str(self.height))
        self.ball.pos = (
            self.center_x - self.ball_size / 2,
            self.center_y - self.ball_size / 2,
        )

    def update(self, dt):
        print("update")
        x, y = self.ball.pos

        x += self.vx
        y += self.vy

        if y + self.ball_size > self.height:
            y = self.height - self.ball_size
            self.vy = -self.vy

        if x + self.ball_size > self.width:
            x = self.width - self.ball_size
            self.vx = -self.vx

        if x < 0:
            x = 0
            self.vx = -self.vx

        if y < 0:
            y = 0
            self.vy = -self.vy

        self.ball.pos = (x, y)


if __name__ == "__main__":
    TheLabApp().run()
