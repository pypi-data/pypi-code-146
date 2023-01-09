def main():
    global randrange
    global turtle
    global square,vector
    global food,snake,aim
    from random import randrange
    import turtle
    from freegames import square, vector
    food = vector(0, 0)
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    turtle.setup(420, 420, 370, 0)
    turtle.hideturtle()
    turtle.tracer(False)
    turtle.listen()
    turtle.onkey(lambda: change(10, 0), 'Right')
    turtle.onkey(lambda: change(-10, 0), 'Left')
    turtle.onkey(lambda: change(0, 10), 'Up')
    turtle.onkey(lambda: change(0, -10), 'Down')
    move()
    turtle.done()
    print('\nTo keep playing the game, keep calling the main function\nElse, Adios amigo/amiga\n')
        

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190


def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'brown')
        turtle.update()
        return

    snake.append(head)
    
    if head == food:
        print('Point:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    turtle.clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'red')
    turtle.update()
    turtle.ontimer(move, 100)
