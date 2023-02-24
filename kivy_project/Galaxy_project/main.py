"""
Un projet pour appronfondir mes connaissances sur le module de python kivy.
Je pourrai aussi continuer a developper de nouvelles application avec ce module.
A present, dans ce module je developpe avec aide le jeu du projet Galaxy.
Ce jeu consiste a deplacer un spaceship sur un plan, et suivre le chemin trace devant soi...
"""

# pylint: disable = wrong-import-order, no-name-in-module, import-outside-toplevel, wrong-import-position

from kivy.config import Config

# configuring the screen which is gonna be opened by kivy
Config.set("graphics", "width", "900")
Config.set("graphics", "height", "400")

import random
from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder

# loading another .kv file...
Builder.load_file("menu.kv")


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
    settings_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("S T A R T")
    score_txt = StringProperty()
    settings_button_title = StringProperty(" S  E  T  T  I  N  G  S")

    V_NB_LINES = 10
    V_LINES_SPACING = 0.4  # percentage in screen width
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = 0.1  # percentage in screen height
    horizontal_lines = []

    SPEED = 0.4
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 3.0
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 16
    tiles = []
    tiles_coordinates = []

    ship = None

    state_game_over = False
    state_game_has_started = False

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

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
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

    def is_desktop(self):
        """
        Methode pour tester le systeme d'exploitation de l'appareil sur lequel est lance le jeu.
        """
        if platform in ("linux", "win", "macosx"):
            return True
        return False

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

    def speed_update(self):
        "In this function we increase the speed of the game."
        actual_speed = self.SPEED
        if self.current_y_loop == 85:
            actual_speed += 0.1
        elif self.current_y_loop == 150:
            actual_speed += 0.1
        elif self.current_y_loop == 400:
            actual_speed += 0.15
        elif self.current_y_loop == 750:
            actual_speed += 0.2
        elif self.current_y_loop == 1000:
            actual_speed += 0.15
        return actual_speed

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
        time_factor = _dt * 60
        speed = self.SPEED
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        # if app.root.current

        if not self.state_game_over and self.state_game_has_started:
            speed_y = speed * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "S  C  O  R  E :  " + str(self.current_y_loop)
                if self.current_y_loop >= 70:
                    speed = self.speed_update()
                self.generate_tiles_coordinates()
                print("actual speed: " + str(speed))
                print("loop : " + str(self.current_y_loop))

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor
            if self.current_y_loop == 1000:
                speed_x += 0.15

        # checking if we are in a game over state, and if the ship hasgone out of the track
        # handling the behavior of the game
        # the game over state is set to True, the opacity of the menu is set t0 0.8,
        # so the menu appears on top of the game window;
        # and the title of the menu screen and the the title of the button is changed.

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 0.8
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.button_title = "R E S T A R T"

            # PLaying the different songs related to the game over state

            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            self.sound_gameover_voice.play()

    def play_game_over_voice_sound(self):
        "a function that plays the game over voice when we are in a game over state"
        if not self.state_game_over:
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
        # print("Button")
        if self.state_game_over:
            self.sound_gameover_voice.stop()
            self.sound_gameover_impact.stop()
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.sound_music1.play()
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0

    def on_settings_button_pressed(self):
        """
        This function handles all the behavior of the settings button which is on the menu page.
        ...
        """


"""
class SettingsWindow(Screen):
    pass


class MenuWindow(Screen):
    pass
"""


class GalaxyApp(App):
    "The main app class"
    menu = MainWidget
    WindowManager = ScreenManager()


"""
    def build(self):
        "..."
        if self.WindowManager.current == "game_screen":
            self.menu.state_game_has_started = True
"""

GalaxyApp().run()
