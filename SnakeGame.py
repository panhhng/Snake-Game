from tkinter import *
from tkinter import ttk
import random

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# constants 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SPACE_SIZE = 50

default_speed = 200

DEFAULT_BODY = 2
SNAKE_COLOR = "#3FFF5C"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = DEFAULT_BODY
        self.location = []
        self.squares = []

        for i in range(0, DEFAULT_BODY):
            self.location.append([0, 0])

        for x, y in self.location:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int((SCREEN_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((SCREEN_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE

        self.location = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.location[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE

    snake.location.insert(0,(x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.location[0] and y == food.location[1]:
        global score
        score += 1
        canvas.delete("food")
        label.config(text="Score: {}".format(score))
        food = Food()
    else:
        del snake.location[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if isCollide(snake):
        endGame()
    else:
        window.after(default_speed, next_turn, snake, food)

def changeDir(newDir):
    global direction

    if newDir == 'left':
        if direction != 'right':
            direction = newDir
    if newDir == 'right':
        if direction != 'left':
            direction = newDir
    if newDir == 'up':
        if direction != 'down':
            direction = newDir
    if newDir == 'down':
        if direction != 'up':
            direction = newDir
    
def isCollide(snake):
    x, y = snake.location[0]

    if x < 0 or x >= SCREEN_WIDTH:
        return True
    elif y < 0 or y >= SCREEN_HEIGHT:
        return True 
    
    for bodyPart in snake.location[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True
        
    return False

def endGame():
    reButton = Button(window, text="Restart", command=lambda: (canvas.delete(ALL), reButton.destroy(), replay()), font=('consolas', 40))
    reButton.place(x=250, y=250)
    
def replay():
    global snake, food, score, direction

    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    next_turn(snake, food)
 
def on_combobox_select(event):
    selected_speed = cbSpeed.get()
    global default_speed
    
    if selected_speed == "Easy":
        default_speed = 200
    elif selected_speed == "Medium":
        default_speed = 150
    else:
        default_speed = 100   

window = Tk()
window.title("Xenzia")
window.resizable(False, False)

choices = ['Easy', 'Medium', 'Hard']
cbSpeed = ttk.Combobox(window, values=choices)
cbSpeed.pack(side=TOP, padx=10, pady=5)

cbSpeed.set("Easy")

cbSpeed.bind("<<ComboboxSelected>>", on_combobox_select)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (int)((screen_width / 2) - (window_width / 2))
y = (int)((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: changeDir('left'))
window.bind('<Right>', lambda event: changeDir('right'))
window.bind('<Up>', lambda event: changeDir('up'))
window.bind('<Down>', lambda event: changeDir('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()