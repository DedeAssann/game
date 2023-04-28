# pylint: disable = missing-class-docstring, import-outside-toplevel, unused-import, invalid-name, missing-function-docstring, no-name-in-module, pointless-string-statement, wrong-import-position

"""
The transformation functions have been transferred from the main file, to this one
"""
from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "left":
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == "right":
        self.current_speed_x = -self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True


def on_touch_down(self, touch):
    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width / 2 and self.height * 0.1 < touch.y < self.height * 0.9:
            self.current_speed_x = self.SPEED_X
        elif (
            touch.x > self.width / 2 and self.height * 0.1 < touch.y < self.height * 0.9
        ):
            self.current_speed_x = -self.SPEED_X
        else:
            pass
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    # print("UP")
    self.current_speed_x = 0
