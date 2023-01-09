"""
 _summary_

Dans ce module on va essayer de coder le Pong Game, avec l'aide
d'un guide sur internet, et en utilisant le module Kivy.
On part pour une nouvelle aventure!

_extended_summary_
"""
# pylint: disable= import-error

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint
from kivy import Config

kivy.require("1.9.0")
Config.set("graphics", "multisamples", "0")


class PongPaddle(Widget):
    """
    La classe qui va gerer les paddles du jeu
    """
    score = NumericProperty(0)
    
    def bounce_ball(self, ball):
        "a bouncing method for the ball"
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            

class PongBall(Widget):
    """
    La classe qui va gerer principalement la balle du jeu
    """
    
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    # using ball.velocity as a property
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # move function will move the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    


class PongGame(Widget):
    """
    the main class
    """
    ball = ObjectProperty(None)
    
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
    
    def update(self, dt):
        
        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > 0):
            self.ball.veloctity *= -1
            
        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1


class PongApp(App):
    """
    La classe qui va gerer le jeu as an administrator
    """
    
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60)
        return game
    
    
    
if __name__ == "__main__":
    PongApp().run()


