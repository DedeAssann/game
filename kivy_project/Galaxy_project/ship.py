"In this module we handle all about the ship components in the game"

# pylint: disable = no-name-in-module

from typing import List
from xmlrpc.client import Boolean
from kivy.graphics.vertex_instructions import Triangle
from kivy.graphics.context_instructions import Color


SHIP_WIDTH = 0.1
SHIP_HEIGHT = 0.035
SHIP_BASE_Y = 0.04
ship_coordinates = [(0, 0), (0, 0), (0, 0)]


def init_ship(self):
    """Initialisation du vaisseau spatial"""
    with self.canvas:
        Color(0, 0, 0)
        self.ship = Triangle()


def update_ship(self) -> List:
    """Mise a jour du mouvement/position du vaisseau spatial"""
    center_x = self.width / 2
    base_y = SHIP_BASE_Y * self.height
    ship_half_width = SHIP_WIDTH * self.width / 2
    ship_height = SHIP_HEIGHT * self.height
    # ....
    #    2
    #  1   3
    # self.transform
    ship_coordinates[0] = (center_x - ship_half_width, base_y)
    ship_coordinates[1] = (center_x, base_y + ship_height)
    ship_coordinates[2] = (center_x + ship_half_width, base_y)
    x_1, y_1 = self.transform(*ship_coordinates[0])
    x_2, y_2 = self.transform(*ship_coordinates[1])
    x_3, y_3 = self.transform(*ship_coordinates[2])
    self.ship.points = [x_1, y_1, x_2, y_2, x_3, y_3]


def check_ship_collision(self) -> Boolean:
    """
    Here we check if the ship if colliding with a tile.
    We use the check_ship_collision_with_tile to do that.
    """
    for i, _ in enumerate(self.tiles_coordinates):
        ti_x, ti_y = self.tiles_coordinates[i]
        if ti_y > self.current_y_loop + 1:
            return False
        if check_ship_collision_with_tile(self, ti_x, ti_y):
            return True
    return False


def check_ship_collision_with_tile(self, ti_x, ti_y) -> Boolean:
    """
    In this function we check if the ship is still on the track.
    To do so, we get the ship coordinates and check if at least one of them is on the current tile.
    """

    xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
    xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
    for _ in range(0, 3):
        p_x, p_y = ship_coordinates[_]
        if xmin <= p_x <= xmax and ymin <= p_y <= ymax:
            return True
    return False
