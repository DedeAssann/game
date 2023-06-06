from turtle import *
from math import cos, sin


def hearta(k):
    return 15 * sin(k) ** 3


def heartb(k):
    return 12 * cos(k) - 5 * cos(2 * k) - 2 * cos(3 * k) - cos(4 * k)


speed(0)
bgcolor("black")
for i in range(10000):
    goto(hearta(i) * 20, heartb(i) * 20)
    for j in range(5):
        color("#f73487")
    goto(0, 0)

done()
