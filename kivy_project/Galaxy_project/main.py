"""
Un projet pour appronfondir mes connaissances sur le module de python kivy.
Je pourrai aussi continuer a developper de nouvelles application avec ce module.
A present, dans ce module je developpe avec aide le jeu du projet Galaxy.
Ce jeu consiste a deplacer un spaceship sur un plan, et suivre le chemin trace devant soi...
"""

# pylint: disable = wrong-import-order, no-name-in-module, import-outside-toplevel, wrong-import-position


from kivy.config import Config

from tuto import FirstWindow, SecondWindow, Tutorial

# configuring the screen which is gonna be opened by kivy
Config.set("graphics", "width", "1200")
Config.set("graphics", "height", "650")
Config.set("graphics", "resizable", True)

from kivy.core.window import Window

Window.allow_screensaver = True

import cProfile
import random
from kivy import platform

from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    StringProperty,
    BooleanProperty,
    Clock,
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.image import Image
from kivy.lang.builder import Builder

# from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore

# loading another .kv file...
Builder.load_file("menu.kv")
Builder.load_file("settings.kv")
Builder.load_file("tuto.kv")

store = JsonStore("myapp.json")


class MainWidget(RelativeLayout):
    """
    Cette classe gere tout le jeu.
    L'initialisation de tous les elements graphiques du jeu, ainsi que leur mise a jour.
    """

    from transforms import transform
    from user_actions import (
        keyboard_closed,
        on_keyboard_up,
        on_keyboard_down,
        on_touch_up,
        on_touch_down,
    )
    from sounds import init_audio
    from ship import (
        init_ship,
        update_ship,
        check_ship_collision,
    )

    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    menu_widget = ObjectProperty()
    pause_button = ObjectProperty()
    pause_widget = ObjectProperty()

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    score = NumericProperty(0)
    best_score = NumericProperty(0)

    score_txt = StringProperty()
    best_score_txt = StringProperty()
    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("S T A R T")
    settings_button_title = StringProperty(" S  E  T  T  I  N  G  S")
    pause_button_txt = StringProperty("P A U S E")

    pause_state = BooleanProperty(False)
    state_game_over = BooleanProperty(False)
    state_game_has_started = BooleanProperty(False)
    game_is_playing_state = BooleanProperty(False)

    V_NB_LINES = 10
    V_LINES_SPACING = 0.5  # percentage in screen width
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = 0.1  # percentage in screen height
    horizontal_lines = []

    SPEED = 0.3
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = NumericProperty(3.0)
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 16
    tiles = []
    tiles_coordinates = []

    ship = None

    fps = NumericProperty(60)

    def __init__(self, **kwargs):
        """
        Methode d'initialisation.
        Ici, nous initialisons les elements graphiques du jeu, tel que le spaceship, le plan
        graphique du jeu. Nous faisons aussi derouler les etapes du chemin a suivre
        (ce qui est genere de maniere aleatoire).
        """
        super().__init__(**kwargs)
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()
        self.speed_update()

        if App.get_running_app().is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        else:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_touch_down)
            self._keyboard.bind(on_key_up=self.on_touch_up)

        Clock.schedule_interval(self.update, 1.0 / self.fps)
        self.sound_galaxy.play()

    def reset_game(self):
        "Here we reset the main variables of the game, so we can restart the game."

        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.score_txt = " S  C  O  R  E :  " + str(self.current_y_loop)
        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False

    def init_tiles(self):
        """
        Initialisation du chemin a suivre
        """
        with self.canvas:
            Color(1, 1, 1)
            for _ in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        """Chemin de depart"""
        for _ in range(0, 18):
            self.tiles_coordinates.append((0, _))

    def generate_tiles_coordinates(self):
        """
        Generation automatique du chemin a suivre, apres l'initialisation
        """
        last_x = 0
        last_y = 0

        # clean the coordinates that are out of the screen
        # ti_y < self.current_y_loop
        for _ in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[_][1] < self.current_y_loop:
                del self.tiles_coordinates[_]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        # print("foo1")

        for _ in range(len(self.tiles_coordinates), self.NB_TILES):
            rand_value = random.randint(0, 2)
            # 0 -> straight
            # 1 -> right
            # 2 -> left
            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1
            if last_x <= start_index:
                rand_value = 1
            if last_x + 1 >= end_index:
                rand_value = 2

            self.tiles_coordinates.append((last_x, last_y))
            if rand_value == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if rand_value == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            last_y += 1

        # print("foo2")

    def init_vertical_lines(self):
        """
        Initalisation des lignes verticales du graphique
        """
        with self.canvas:
            Color(1, 1, 1)
            for _ in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        "A simple method to get the line x by its index"
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        "A simple method to get the line_y by its index"
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        """
        Generation automatique des etapes a suivre pour le chemin
        """
        ti_y = ti_y - self.current_y_loop
        _x = self.get_line_x_from_index(ti_x)
        _y = self.get_line_y_from_index(ti_y)
        return _x, _y

    def update_tiles(self):
        """
        Mise a jour du chemin
        """
        for _ in range(0, self.NB_TILES):
            tile = self.tiles[_]
            tile_coordinates = self.tiles_coordinates[_]
            xmin, ymin = self.get_tile_coordinates(
                tile_coordinates[0], tile_coordinates[1]
            )
            xmax, ymax = self.get_tile_coordinates(
                tile_coordinates[0] + 1, tile_coordinates[1] + 1
            )
            #  2    3
            #
            #  1    4
            x_1, y_1 = self.transform(xmin, ymin)
            x_2, y_2 = self.transform(xmin, ymax)
            x_3, y_3 = self.transform(xmax, ymax)
            x_4, y_4 = self.transform(xmax, ymin)

            tile.points = [x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4]

    def update_vertical_lines(self):
        """
        Mise a jour des lignes verticales du graphique
        """
        # -1 0 1 2
        start_index = -int(self.V_NB_LINES / 2) + 1
        for _ in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(_)

            x_1, y_1 = self.transform(line_x, 0)
            x_2, y_2 = self.transform(line_x, self.height)
            self.vertical_lines[_].points = [x_1, y_1, x_2, y_2]

    def init_horizontal_lines(self):
        """
        Initialisation des lignes horizontales du graphique
        """
        with self.canvas:
            Color(1, 1, 1)
            for _ in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        """
        Mise a jour des lignes horizontales du graphique
        """
        start_index = -int(self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for _ in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(_)
            x_1, y_1 = self.transform(xmin, line_y)
            x_2, y_2 = self.transform(xmax, line_y)
            self.horizontal_lines[_].points = [x_1, y_1, x_2, y_2]

    def update_pause_button_txt(self):
        """
        ...
        """
        if self.pause_state is False:
            self.pause_button_txt = "P A U S E"
        if self.pause_state is True:
            self.pause_button_txt = "R E S U M E"

    def speed_update(self):
        "In this function we increase the speed of the game."
        # actual_speed = 0.4

        if self.current_y_loop == 49:
            self.SPEED += 0.075
        elif self.current_y_loop == 99:
            self.SPEED += 0.075
        elif self.current_y_loop == 149:
            self.SPEED += 0.05
        elif self.current_y_loop == 249:
            self.SPEED += 0.05
        elif self.current_y_loop == 399:
            self.SPEED += 0.04
        elif self.current_y_loop == 549:
            self.SPEED += 0.04
        elif self.current_y_loop == 699:
            self.SPEED += 0.03
        elif self.current_y_loop == 859:
            self.SPEED += 0.03
        elif self.current_y_loop == 1099:
            self.SPEED += 0.02

    def get_speed(self):
        "..."
        self.SPEED = (
            0.3
            + self.parent.manager.settings_window.settings_widget.stack.l_8.my_slider.value
            / 10
        )
        print(self.SPEED)

    def update(self, _dt):
        """
        Mise a jour periodique du jeu et de tous ces composants.
        In this function we call every other functions that updates a part of the game,
        and this update function is called recursively and periodically.
        It is precisely called every 1/60 second.
        Here we update the vertical and horizontal lines, the tiles and the position of the ship.
        Here we also handle the behavior of the game when it is playing and when it's not;
        in other words, when we are in a game over state and when we are not.
        """

        # Updating the different graphical components of the game, such as the vertical and
        # horizontal lines the tiles and the ship.

        self.fps = self.parent.manager.get_screen(
            "settings_screen"
        ).ids.settings_widget.stack.l_3.max_fps
        time_factor = _dt * self.fps
        # print(self.fps)
        # print(self.SPEED)
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        # pause button behavior
        if not self.state_game_over:
            self.pause_button.disabled = False
            self.pause_button.opacity = 1

        if not self.state_game_has_started:
            self.pause_button.opacity = 0
            self.pause_button.disabled = True
            # setting the pause widget opacity to 0 at startup
            self.pause_widget.opacity = 0

        if self.state_game_over:
            self.pause_button.opacity = 0
            self.pause_button.disabled = True

        # updating the game
        if (
            not self.state_game_over
            and self.state_game_has_started
            and not self.pause_state
        ):
            self.game_is_playing_state = True
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "S C O R E :  " + str(self.current_y_loop)
                if self.current_y_loop >= 9:
                    self.speed_update()
                self.generate_tiles_coordinates()
                print("actual speed: " + str(self.SPEED))
                print("loop : " + str(self.current_y_loop))

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

        # checking if we are in a game over state, and if the ship hasgone out of the track
        # handling the behavior of the game
        # the game over state is set to True, the opacity of the menu is set t0 0.8,
        # so the menu appears on top of the game window;
        # and the title of the menu screen and the the title of the button is changed.

        if not self.check_ship_collision() and not self.state_game_over:
            self.game_is_playing_state = False
            self.state_game_over = True
            self.menu_widget.opacity = 0.9
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "R E S T A R T"
            self.score = self.current_y_loop

            # PLaying the different songs related to the game over state
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            self.sound_gameover_voice.play()
            Clock.schedule_once(self.play_game_over_voice_sound, 0)
            # print("GAME OVER")

            # writing the scores
            score = self.current_y_loop
            App.get_running_app().write_scores(score)

    def on_pause_button_pressed(self):
        "..."
        self.pause_state = not self.pause_state
        # print(f" pause state : {self.pause_state}")
        if self.pause_state:
            self.game_is_playing_state = False
            global actual_speed
            actual_speed = self.SPEED
            self.SPEED = 0
            self.update_pause_button_txt()
            self.sound_music1.stop()
            self.pause_widget.opacity = 0.7
        elif not self.pause_state and not self.state_game_over:
            self.game_is_playing_state = True
            self.SPEED = actual_speed
            self.update_pause_button_txt()
            self.pause_widget.opacity = 0
            self.sound_music1.play()
        else:
            pass

    def play_game_over_voice_sound(self, dt):
        "a function that plays the game over voice when we are in a game over state"
        if self.state_game_over:
            self.sound_gameover_voice.play()

    def on_menu_button_pressed(self):
        """
        This function handles all the behavior of the game when we press the start/restart button.
        If we are in a game over state and we press the button, it will play the begin sound;
        If we are not in a game over state and we press the button it'll stop playing the game over
        sounds and play the restart sound.
        It also reset all the variables in the game, such as the self.state_game_has_started is set
        to True, the opacity of the menu widget is set to 0 and the main theme of the game is played
        """
        if self.state_game_over:
            self.sound_gameover_voice.stop()
            self.sound_gameover_impact.stop()
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.sound_music1.play()
        self.reset_game()
        self.get_speed()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0


# the GameWindow class
class GameWindow(Screen):
    "The screen that carries the MainWidget interface"

    main_widget = ObjectProperty()
    home_button = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.on_progress, 1.0 / 60)

    def on_progress(self, _dt):
        "..."
        if self.main_widget.game_is_playing_state:
            self.home_button.opacity = 0
            self.home_button.disabled = True
        else:
            self.home_button.opacity = 1
            self.home_button.disabled = False


# the pause Widget class
class PauseWidget(RelativeLayout):
    "..."


# the HomeWindow class
class HomeWindow(Screen):
    "The first screen displayed!"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.starship = Image(
            source="spaceship_models\spaceship6_edited.png",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.45, 0.4),
            allow_stretch=True,
        )
        # self.add_widget(self.starship)

    def exit(self, *args):
        "Implementing an exit function for the game"
        App.get_running_app().stop()


# The Settings Window
class SettingsWindow(Screen):
    "..."

    settings_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# the WindowManager class
class WindowManager(ScreenManager):
    "..."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        transition = NoTransition(duration=0)
        self.transition = transition


# The App
class GalaxyApp(App):
    """The main app class"""

    use_kivy_settings = False
    title = "|             M   y      G   a   l   a   x   y      J   o   u   r   n   e   y              |".upper().ljust(
        300
    )
    store = store
    profile = cProfile.Profile()
    icon = "galaxy_images/download.jpg"
    name = "G A L A X Y"

    def progress_empty(self):
        if (
            self.store.get("Score")["value"] == 0
            and self.store.get("Best Score")["value"] == 0
            and self.store.get("Name of User")["value"] == ""
            and self.store.get("Age of User")["value"] == ""
            and self.store.get("Mail of User")["value"] == ""
            and self.store.get("Level")["value"] == 0.0
            and self.store.get("Current FPS Level")["value"] == 60
            and self.store.get("Max FPS Level")["value"] == 60
            and self.store.get("Song State")["value"] is True
            and self.store.get("Song Volume")["value"] == 50
            and self.store.get("Music State")["value"] is True
            and self.store.get("Music Volume")["value"] == 50
            and self.store.get("SFX Volume")["value"] == 50
            and self.store.get("SFX State")["value"] is True
        ):
            progress = False
        else:
            progress = True
        return progress

    def reset_progress(self):
        self.store.put("Score", name="Score", value=0)
        self.store.put("Best Score", name="Best Score", value=0)
        self.store.put("Name of User", name="Name", value="")
        self.store.put("Age of User", name="Age", value="")
        self.store.put("Username", name="Username", value="")
        self.store.put("Mail of User", name="Mail", value="")
        self.store.put("Level", name="Level", value=0.0)
        self.store.put("Current FPS Level", name="FPS", value=60)
        self.store.put("Max FPS Level", name="limit FPS", value=60)
        self.store.put("Song State", name="Song State", value=True)
        self.store.put("Song Volume", name="Song Volume", value=50)
        self.store.put("Music State", name="Music State", value=True)
        self.store.put("Music Volume", name="Music Volume", value=50)
        self.store.put("SFX Volume", name="SFX Volume", value=50)
        self.store.put("SFX State", name="SFX State", value=True)
        self.store.put("Language", name="Language", value="en")

    def write_scores(self, score):
        self.store.put("Score", name="Score", value=score)
        if score > self.store.get("Best Score")["value"]:
            best_score = score
            self.store.put("Best Score", name="Best Score", value=best_score)
        else:
            pass

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] is "escape":
            pass

    def is_desktop(self):
        """
        Methode pour tester le systeme d'exploitation de l'appareil sur lequel est lance le jeu.
        """
        if platform in ("linux", "win", "macosx"):
            return True
        return False

    def open_settings(self, *largs):
        pass

    def on_start(self):
        self.is_desktop()
        # print(self.progress_empty())
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats("tryapp.profile")

    def on_pause(self):
        return True

    def on_resume(self):
        pass


GalaxyApp().run()
