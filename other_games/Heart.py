"A sikmple script that can make a heart"

import turtle
from turtle import *
from math import cos, sin

turtle.Screen().setup(width=0.5, height=0.75, startx=None, starty=None)
pen = turtle.Turtle()


def curve():
    "fe curve"
    # Defining step by step
    pen.speed(25)
    for i in range(200):
        pen.right(1)
        pen.forward(1)


# Defining method to write text
def text():
    # Move turtle to the air
    pen.up()
    # Move turtle to a given position
    pen.setpos(-62, 95)
    # Move turtle to the ground
    pen.down()
    # Set the color of the pen
    pen.color("lightgreen")
    # Write the specified text
    # specified font style and size
    pen.write("I LuV U Sweetie", font=("Verdana", 12, "bold"))


# Defining method to draw a full heart
def heart():
    pen.speed(25)
    pen.fillcolor("black")
    pen.begin_fill()
    # Draw the left line
    pen.left(140)
    pen.forward(113)
    # Draw the left curve
    curve()
    pen.left(120)
    # Draw the right curve
    curve()
    # Draw the right line
    pen.fd(112)
    # Ending the fill of the heart
    pen.end_fill()


def make_heart():
    "Create a heart"
    # Draw the heart
    heart()
    # Write the text
    text()
    # To hide turtle
    pen.ht()

    bgcolor("red")
    turtle.Screen().exitonclick()


if __name__ == "__main__":
    make_heart()
