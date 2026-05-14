
import turtle
from math import *

def carre():
    "fe yon carre..."
    carre = turtle.Turtle() 
    # Defining the square step by step
    carre.speed(10)
    carre.color("blue", "lightblue")
    carre.begin_fill()
    for i in range(4):
        carre.fd(200)
        carre.left(90)
    carre.end_fill()
    turtle.done()
    
def star():
    "fe yon etoile"
    star.color("red", "yellow")
    star.speed(10)
    star.begin_fill()
    for i in range(108):
        star.fd(300)
        star.left(170)
    star.end_fill()
    turtle.done()
    
# Defining an object
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
    pen.write("I LuV U Djounie", font=("Verdana", 12, "bold"))

# Defining method to draw a full heart
def heart():
    pen.speed(25)
    pen.fillcolor("red")
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
    
    
    
# Mpral eseye ekri rapidement on program kap ka fe yon kay ak module turtle lan

def kay():
    # facade
    for i in range(2):
        pen.fd(100)
        pen.left(90)
        pen.fd(150)
        pen.left(90)
    pen.setpos(40, 0)
    pen.left(90)
    # porte avant
    pen.fd(50)
    pen.right(90)
    pen.fd(20)
    pen.right(90)
    pen.fd(50)
    # le toit
    pen.left(90)
    pen.fd(40)
    pen.left(90)
    pen.fd(150)
    pen.left(55)
    pen.fd(100.4938646)
    pen.left(70)
    pen.fd(100.4938646)
    # Side1
    pen.backward(100.4938646)
    pen.left(35)
    pen.fd(250)
    pen.right(90)
    
    
    pen.left(35)
    pen.fd(250)
    pen.left(145)
    pen.fd(150)
    pen.left(145)
    pen.fd(250)
    # Side2
    pen.setpos(pic)
# Hide the pen
pen.ht()




    