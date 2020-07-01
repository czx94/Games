from tkinter import *
from random import randint

from threading import Thread
import time

def get_point(x, y):
    return x, y, x+10, y+10

def is_rect_overlap(p1, p2):
    if p1 == p2:
        return True
    else:
        return False


class Game(Tk):
    def __init__(self):
        super(Game, self).__init__()
        self.title = "Snake Game"
        self.width = 500
        self.height = 500
        self.next_point = False
        self.points = 3
        self.speed = 1

        self._display_zone = Canvas(self, width=self.width, height=self.height, bg="#fff")
        self._display_zone.pack()

        self._init_modules()
        self._init_game()


    def _init_modules(self):
        self._info_display = Label(self)
        self._info_display.pack(side=TOP)
        self._info_display.config(text=f"Points: {self.points}, speed: {self.speed}")
        # set restart and quit button
        f1 = Frame(self)
        f1.pack(side=TOP, padx=0, pady=5)
        self.restart_button = Button(f1, text='New game', command=self._init_game, width=15).pack(side=LEFT, padx=5,
                                                                                                pady=5)
        self.quit_button = Button(f1, text='Quit', command=self.destroy, width=15).pack(side=LEFT, padx=5, pady=5)

    def _init_game(self):
        self.points = 3
        self.speed = 1
        self.state = True
        self.food = Food(self)
        self.snake = Snake(self)
        self.bind_keys()
        print("Start")
        self.handle()

    def _draw(self):
        print("draw")
        self.food._draw()
        self.snake._draw()
        self._info_display.config(text=f"Points: {self.points}, speed: {self.speed}")

    def bind_keys(self):
        self.bind('<Key-Left>', self.snake.key_press)
        self.bind('<Key-Right>', self.snake.key_press)
        self.bind('<Key-Up>', self.snake.key_press)
        self.bind('<Key-Down>', self.snake.key_press)

    def handle(self):
        if self.state == False:
            self._display_zone.delete(ALL)
            print("Over")
        else:
            if self.next_point:
                self._draw()
                self.next_point = False

class Drawable(object):
    def __init__(self, color, display_zone, erase_color="white"):
        self._display_zone = display_zone
        self._color = color
        self._body = list()

        self._erase_color = erase_color
        self._erase_body = list()

    def _draw(self):
        # draw new points
        for item in self._body:
            self._display_zone.create_rectangle(get_point(*item), fill=self._color, outline="")

        # erase old points
        for item in self._erase_body:
            self._display_zone.create_rectangle(get_point(*item), fill=self._erase_color, outline="")
        self._erase_body = list()


class Snake(Thread, Drawable):
    def __init__(self, game):
        Thread.__init__(self)
        Drawable.__init__(self, "blue", game._display_zone)
        self._game = game
        self._body = [(10, 0), (20, 0), (30, 0)]
        self._current_dir = 'Right'
        self._width = self._game.width
        self._height = self._game.height
        self._sleep_time = 0.25

        self.start()

    def run(self):
        if not self._game.state:
            self._erase_body = self._body
            self._body = list()

        while self._game.state:
            if not self._game.next_point:
                print("move")
                self._move()
                self._game.next_point = True
                self._game.handle()

            time.sleep(self._sleep_time/self._game.speed)

    def _move(self):
        # move
        np = self._next_point()
        print('snake head: ', np)
        if np in self._body or np[0] < 0 or np[0] >= self._width or np[1] < 0 or np[1] >= self._height:
            self._game.state = False
        else:
            if not is_rect_overlap(np, self._game.food._body[0]):
                self._erase_body.append(self._body.pop(0))
            else:
                self._game.points += 1
                self._game.food.generate_point()
            self._body.append(np)
        print(self._body)

    def key_press(self, event):
        current_click = event.keysym
        if current_click == self._current_dir:
            self._game.speed *= 2
        else:
            self._game.speed = 1
            self._current_dir = current_click

    def _next_point(self):
        cur_x, cur_y = self._body[-1]

        if self._current_dir == 'Left':
            cur_x -= 10
        if self._current_dir == 'Up':
            cur_y -= 10
        if self._current_dir == 'Right':
            cur_x += 10
        if self._current_dir == 'Down':
            cur_y += 10
        return cur_x, cur_y


class Food(Drawable):
    def __init__(self, game):
        Drawable.__init__(self, "red", game._display_zone)
        self._game = game
        self._body = [(50, 50)]

    def generate_point(self):
        self._erase_body = self._body
        self._body = [(10*randint(0, self._game.width//10), 10*randint(0, self._game.height//10))]


if __name__ == '__main__':
    w = Game()
    w.mainloop()


