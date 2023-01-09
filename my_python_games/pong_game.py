"trynna code a simple game..."

import turtle as t
import os

PLAYER_A_SCORE = 0
PLAYER_B_SCORE = 0
BALL_X_DIR = 0.2
BALL_Y_DIR = 0.2
# Creating the window object
window = t.Screen()
# Setting right and left paddles
rightpaddle = t.Turtle()
leftpaddle = t.Turtle()
# Create the ball object
ball = t.Turtle()
# Creating a pen object
pen = t.Turtle()

def setup():
    "create a window and declare a variable called window and call the screen()"
    window.title("The Pong Game")
    window.bgcolor("green")
    window.setup(width=800,height=600)
    window.tracer(0)

    #Creating the left paddle
    leftpaddle.speed(25)
    leftpaddle.shape("square")
    leftpaddle.color("white")
    leftpaddle.shapesize(stretch_wid=5,stretch_len=1)
    leftpaddle.penup()
    leftpaddle.goto(-350,0)

    #Creating the right paddle
    rightpaddle.speed(0)
    rightpaddle.shape("square")
    rightpaddle.color("white")
    rightpaddle.shapesize(stretch_wid=5,stretch_len=1)
    rightpaddle.penup()
    rightpaddle.goto(-350,0)

    #Code for creating the ball
    ball.speed(0)
    ball.shape("circle")
    ball.color("red")
    ball.penup()
    ball.goto(5,5)

    "Code for creating pen for scorecard update"
    pen.speed(0)
    pen.color("Blue")
    pen.penup()
    pen.hideturtle()
    pen.goto(0,260)
    pen.write("score",align="center",font=('Arial',24,'normal'))

# pylint: disable = missing-function-docstring
#code for moving the leftpaddle
def leftpaddleup():
    y = leftpaddle.ycor()
    y += 90
    leftpaddle.sety(y)

def leftpaddledown():
    y = leftpaddle.ycor()
    y += 90
    leftpaddle.sety(y)

#code for moving the rightpaddle
def rightpaddleup():
    y = rightpaddle.ycor()
    y += 90
    rightpaddle.sety(y)

def rightpaddledown():
    y = rightpaddle.ycor()
    y += 90
    rightpaddle.sety(y)

#Assign keys to play
def game():
    
    setup()
    
    window.onkeypress(leftpaddleup,'w')
    window.onkeypress(leftpaddledown,'s')
    window.onkeypress(rightpaddleup,'Up')
    window.onkeypress(rightpaddledown,'Down')
    window.listen()

    while True:
        window.update()

        #moving the ball
        ball.setx(ball.xcor()+BALL_X_DIR)
        ball.sety(ball.ycor()+BALL_X_DIR)

        #border set up
        if ball.ycor()>290:
            ball.sety(290)
            BALL_Y_DIR = BALL_Y_DIR * -1
        if ball.ycor()<-290:
            ball.sety(-290)
            BALL_Y_DIR = BALL_Y_DIR * -1

        if ball.xcor() > 390:
            ball.goto(0,0)
            ball_dx = ball_dx * -1
            PLAYER_A_SCORE = PLAYER_A_SCORE + 1
            pen.clear()
            pen.write(f"Player A: {PLAYER_A_SCORE}                    Player B: {PLAYER_B_SCORE} ", align = "center", font = ('Monaco', 24, "normal"))
            os.system("afplay wallhit.wav&")



        if(ball.xcor()) < -390: # Left width paddle Border
            ball.goto(0,0)
            ball_dx = ball_dx * -1
            PLAYER_B_SCORE = PLAYER_B_SCORE + 1
            pen.clear()
            pen.write(f"Player A: {PLAYER_A_SCORE}                    Player B: {PLAYER_B_SCORE} ", align = "center", font = ('Monaco', 24, "normal"))
            os.system("afplay wallhit.wav&")

        # Handling the collisions with paddles.

        if(ball.xcor() > 340) and (ball.xcor() < 350) and (ball.ycor() < rightpaddle.ycor() + 40 and ball.ycor() > rightpaddle.ycor() - 40):
            ball.setx(340)
            ball_dx = ball_dx * -1
            os.system("afplay paddle.wav&")

        if(ball.xcor() < -340) and (ball.xcor() > -350) and (ball.ycor() < leftpaddle.ycor() + 40 and ball.ycor() > leftpaddle.ycor() - 40):
            ball.setx(-340)
            ball_dx = ball_dx * -1
            os.system("afplay paddle.wav&")