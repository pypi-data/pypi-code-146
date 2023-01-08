"""
this simple program can make terminal figure output.
Note: that this does not make an app or ui with the figure in it
"""
#imports:
import time



#this is a simple lite program to make a line
def line(flush=bool(True), times=int(15), delay=float(0.1)):
    """
    this will make a simple line, just like a loadingbar, but diffrent

    flush:  just like print, this will look cooler
    times:  how many times "-" to be printed
    delay:  this will make a delay before every print, needs flush=True

    this will make something like this: ------------------
    this uses the default color, so there is no color change
    """

    for x in range(times):
        print("-", sep="", end="", flush=flush)
        time.sleep(delay)


#simple rect that can take in width and height input but it is only in int
def sRect(width=int(10), height=int(10), xPos=int(20), delay=float(0.0)):
    """
    This can make a rect, (sRect = simple Rect)

    width:    a int that sets the width of the triangle
    height:   a int that sets the height of the triangle
    xPos:     this will let you .rjust the rectangle
    delay:    this is to make the rect print the midle slowly

    width and height is set to 10 by default, that will make ----------
    with an ecual height
    """
    #make the top and bottom
    t = ""
    for x in range(width + 1):
        t = t + "-"
    
    #here we print the top
    print(t.rjust(xPos))
    
    #this will make the sides
    prev = 0
    for x in range(height):
        s = ""
        if prev == 0:
            prev = x
        elif x - prev == 2:
            s = s + ("|" + "|".rjust(width))
            #here we print the side
            print(s.rjust(xPos))
            
            prev = x
            time.sleep(delay)
    
    #here we print the bottom
    print(t.rjust(xPos))