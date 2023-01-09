import math
import time
from turtle import *
import turtle
import random
def new_grp():
    ws = turtle.Screen()
    ws.setup(900, 800)
    txt=turtle.textinput("2K23 QUOTES","Enter your Name :")
    hideturtle()
    quot=["The only one who can tell you “you can’t win” is you and you don’t have to listen","Set your goals high, and don’t stop till you get there.","Life is like riding a bicycle. To keep your balance you must keep moving","I have never let my schooling interfere with my education.","If you can’t yet do great things, do small things in a great way.","Be sure you put your feet in the right place, then stand firm.","Do not wait for the perfect time and place to enter, for you are already onstage.","The greater the difficulty, the more the glory in surmounting it.","I never look back, darling. It distracts from the now.","A year from now you will wish you had started today.","I never dreamed about success. I worked for it","Success is getting what you want, happiness is wanting what you get.","Don’t let yesterday take up too much of today.","Goal setting is the secret to a compelling future.","Either you run the day or the day runs you.","Make sure your worst enemy doesn’t live between your own two ears.","Hustle beats talent when talent doesn’t hustle","Start where you are. Use what you have. Do what you can.","We are what we repeatedly do. Excellence, then, is not an act, but a habit.","Setting goals is the first step in turning the invisible into the visible."]
    q=random.choice(quot)
    speed(0)
    pensize(10)
    colormode(255)
    while True:
        turtle.bgcolor("yellow")
        turtle.color("red")
        write(txt + " Happy new Year" , align="center", font=("Cooper Black", 25, "italic"))
        time.sleep(2)
        turtle.clear()
        turtle.color("blue")
        write( "Quote for you : \n"+q, align="center", font=("Cooper Black", 15, "italic"))
        time.sleep(3)
        turtle.clear()
        def hearta(k):
          return 15*math.sin(k)**3
        def heartb(k):
          return 12*math.cos(k)-5*\
                 math.cos(2*k)-2*\
                 math.cos(3*k)-\
                 math.cos(4*k)
          speed(0)
        bgcolor("black")
        for i in range(6000):
          goto(hearta(i)*20,heartb(i)*20)
          for j in range(5):
              color("#f73487")
          goto(0,0)
        done()

