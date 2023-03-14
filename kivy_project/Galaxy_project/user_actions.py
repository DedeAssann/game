# pylint: disable = missing-class-docstring, import-outside-toplevel, unused-import, invalid-name, missing-function-docstring, no-name-in-module, pointless-string-statement, wrong-import-position

"""
The transformation functions have been transferred from the main file, to this one
"""
from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.unbind(on_key_up=self.on_keyboard_up)
    self.keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "left":
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == "right":
        self.current_speed_x = -self.SPEED_X
    return True


def on_keyboard_up(self, _keyboard, keycode):
    self.current_speed_x = 0
    return True


def on_touch_down(self, touch):
    # state_game_over = False
    # state_game_has_started = False

    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    # print("UP")
    self.current_speed_x = 0
