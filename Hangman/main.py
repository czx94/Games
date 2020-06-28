from tkinter import *
import random

from Hangman.form import *

class Hangman(Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman")
        self._display_zone = Canvas(self, width=480, height=320, bg="white")
        self._display_zone.pack(padx=5,pady=5)

        # load words from txt
        self._word_list = self._load_words("words_source/CET4+6_edited.txt")
        self._word = self._renew_word()

        # initialize buttons
        self._init_modules()


    def _init_modules(self):
        # set display info
        self._display = '*' * len(self._word)
        # object to display on the screen
        self._word_display = Label(self)
        self._word_display.pack(side=TOP)
        self._word_display.config(text='Word: ' + self._display)
        self._count = 0

        # set restart and quit button
        f1 = Frame(self)
        f1.pack(side=TOP, padx=0, pady=5)
        self.restart_button = Button(f1, text='New game', command=self._restart, width=15).pack(side=LEFT, padx=5, pady=5)
        self.quit_button = Button(f1, text='Quit', command=self.destroy, width=15).pack(side=LEFT, padx=5, pady=5)

        # set letters' buttons
        self._buttons = list()
        f2 = Frame(self)
        f2.pack(side=TOP, padx=5, pady=5)
        for i in range(26):
            l = chr(ord('A') + i)
            self._buttons.append(myButton(self, f2, l, 4))
            self._buttons[i].config(command=self._buttons[i].click)

        # arrange buttons
        for i in range(4):
            for j in range(7):
                if i * 7 + j <= 25:
                    self._buttons[i * 7 + j].grid(row=i, column=j)

    def action(self, letter):
        '''
        react to button clicks

        :param letter: the letter clicked
        :return:
        '''
        result = False
        letter_list = list(self._display)

        # judge if the letter is in the word
        for i in range(len(self._word)):
            if self._word[i] == letter:
                letter_list[i] = letter
                result = True

        # update display string
        self._display = ''.join(letter_list)
        self._word_display.config(text='Word: ' + self._display)

        if not result:
            hang_man[self._count].display(self._display_zone)
            self._count += 1

        if self._count == len(hang_man):
            self._success(False)
        if self._display == self._word:
            self._success(True)

    def _restart(self):
        '''
        Reset the word and restart
        :return:
        '''
        self._word = self._renew_word()
        self._display = "*" * len(self._word)
        self._word_display.config(text='Word: ' + self._display)
        
        self._count = 0
        self._display_zone.delete(ALL)
        for b in self._buttons:
            b.config(state=NORMAL)

        print(self._word, self._display_word)

    def _renew_word(self):
        word = random.choice(self._word_list).upper()

        # avoid -
        if word.isalpha():
            return word
        else:
            return self._renew_word()

    def _load_words(self, path):
        with open(path, 'r') as f:
            words = f.read()
            words = words.split()

        return words

    def _success(self, result):
        for i in range(26):
            self._buttons[i].config(state=DISABLED)
        if not result:
            self._word_display.config(text='You lose, the answer is : '+self._word)
        else:
            self._word_display.config(text=self._display+' - Great! You win!')

class myButton(Button):
    def __init__(self, object, parent, letter, size):
        Button.__init__(self, master=parent, text=letter,width=size)
        self._object = object
        self._letter = letter

    def click(self):
        self.config(state=DISABLED)
        self._object.action(self._letter)

hang_man = [Rectangle(175,250,'blue',200,5),Rectangle(175,150,'blue',5,200),\
            Rectangle(200,50,'blue',250,5),Rectangle(300,65,'black',1,30),\
            Circle(300,100,'red',40),Rectangle(300,140,'red',4,40),\
            Rectangle(280,125,'red',40,5),Rectangle(320,125,'red',40,5),\
            Rectangle(280,160,'red',40,5),Rectangle(320,160,'red',40,5)]

if __name__ == "__main__":
    game = Hangman()
    game.mainloop()