"In this module we initialize the menu"
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from tuto import TransitionWidget
from kivy.animation import Animation
from kivy.graphics.instructions import *

font = "fonts/gtr.otf"
_ec = (0.282, 0.694, 0.882, 0.8)


class TransitWidget(TransitionWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = ""

    def animate(self, *args):
        anim = Animation(opacity=0, duration=1)
        anim.bind(
            on_progress=lambda *args: setattr(
                App.get_running_app().root,
                "current",
                self.screen,
            )
        )
        anim.start(self)


class MenuWindow(Screen):
    def get_down_button(self):
        sites = self.menu_widget.s_stack.children
        for site in sites:
            if site.s_button.state == "down":
                return site


class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    def on_site_selection(self, widget):
        if widget.state == "down":
            # Retrieving the Image and the Title
            site = self.parent.get_down_button()
            site_img = site.site_img
            # Unhighlighting the widget and setting it's state to "normal"
            # widget.unhighlight()
            widget.state = "normal"
            # self.parent.manager.game_window.main_widget.canvas.after.clear()
            with self.parent.manager.game_window.main_widget.canvas.before:
                self.parent.manager.game_window.main_widget.rect = Rectangle(
                    source=site_img,
                    pos=self.parent.manager.game_window.main_widget.pos,
                    size=self.parent.manager.game_window.main_widget.size,
                )
            self.parent.manager.game_window.main_widget.bind(
                pos=self.update_rect,
                size=self.update_rect,
            )
            site_name = site.container.label.text
            # Giving the site the title
            self.sitepopup = SitesPopup()
            # Creating the Main Layout that the popup's gonna display
            mainlayout = RelativeLayout(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint_x=1,
                size_hint_y=1,
            )
            self.sitepopup.add_widget(mainlayout)
            container = BoxLayout(
                size_hint=(1, 1),
                orientation="vertical",
                padding=dp(15),
                spacing=dp(20),
            )
            mainlayout.add_widget(container)
            container.canvas.before.clear()
            with container.canvas.before:
                container.rounded_rect = RoundedRectangle(source=site_img)
            container.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)

            # Creating a Label
            sitelabel = Label(
                text=site_name,
                font_name=font,
                font_size=dp(90),
                size_hint=(0.8, 0.8),
                # color=_ec,
                opacity=0.3,
                halign="justify",
                valign="center",
                pos_hint={"center_x": 0.5, "center_y": 0.7},
            )

            container.add_widget(sitelabel)

            # Opening the Popup
            SitesPopup.open(self.sitepopup)

            # Creation of the play button
            playbutton = Button(
                text="PLAY",
                background_color=(0, 0, 0, 0),
                size_hint=(0.6, 0.2),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                font_name=font,
                font_size=dp(40),
            )
            playbutton.canvas.before.clear()
            with playbutton.canvas.before:
                Color(0.282, 0.694, 0.882, 0.18)
                playbutton.rounded_rect = RoundedRectangle()
            playbutton.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
            playbutton.bind(on_press=self.switch_to_game)
            playbutton.bind(on_press=self.sitepopup.dismiss)
            container.add_widget(playbutton)

    def update_rect(self, widget, *args):
        x, y = widget.pos
        width, height = widget.size

        widget.rect.pos = widget.pos
        widget.rect.size = widget.size

    def update_rounded_rect(self, widget, *args):
        x, y = widget.pos
        width, height = widget.size
        # Set the corner radius as a fraction of the smallest dimension of the button
        corner_radius = min(width, height) * 0.1
        widget.rounded_rect.pos = widget.pos
        widget.rounded_rect.size = widget.size
        widget.rounded_rect.radius = [corner_radius]

    def switch_to_game(self, widget):
        SitesPopup.dismiss
        sync = TransitWidget()
        sync.screen = "game_screen"
        # self.opacity = 0
        self.parent.add_widget(sync)
        # self.parent.manager.current = "game_screen"


class SpecialButton(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)

    def highlight(self, *args):
        if self.state == "normal":
            self.unhighlight()
        elif self.state == "down":
            self.canvas.after.clear()
            with self.canvas.after:
                Color(0.282, 0.694, 0.884, 0.2)
                self.rounded_rect = RoundedRectangle()
                # Update the position and size of the rounded rectangle to match the button
                x, y = self.pos
                width, height = self.size

                # Set the corner radius as a fraction of the smallest dimension of the button
                corner_radius = min(width, height) * 0.1

                self.rounded_rect.pos = self.pos
                self.rounded_rect.size = self.size
                self.rounded_rect.radius = [corner_radius]
                Color(1, 1, 1, 1)
                self.line = Line(
                    width=dp(2),
                    rounded_rectangle=(self.x, self.y, self.width, self.height, 20),
                    cap="round",
                    joint="round",
                )

    def unhighlight(self):
        if hasattr(self, "rounded_rect") or hasattr(self, "line"):
            self.canvas.after.remove(self.rounded_rect), self.canvas.after.remove(
                self.line
            )
        pass


class Site(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SitesPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.825, 0.875)

    def remove_widgets(self):
        for child in self.content.children:
            self.content.remove_widget(child)


# Creating the start widget


class StartWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
