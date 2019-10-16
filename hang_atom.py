from IPython.display import clear_output
from enum import Enum
import random

class State (Enum): # This tells the program where we are in the game.
    START = 1
    LOADING = 2
    INGAME = 3
    ENDGAME = 4
    LOSTGAME = 5


class Verbum():

    def __init__(self, file_name):
        self.refresh() # refreshes the stats of the game back to their original state
        self.word_bank = self.createDict(file_name)

    def refresh(self):
        self.state = State.START
        self.secret_word =  '' # Actual name of the word, hidden from the user
        self.word = [] # Name of the word displayed in blanks for them to guess. When all the blanks are gone then you win!
        self.count = 7 # How many lives you have left

        self.possible_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        self.guessed_letters = []

    def createDict(self, file_name): # Creates a dictionary from a txt file.

        word_bank = {}

        with open(file_name) as f:
            for line in f:
                (key, val) = line.split(',')
                key = key.strip()
                val = val.strip()
                if key in word_bank:
                    word_bank[key].append(val)
                else:
                    word_bank[key]= [val]

        return word_bank

    def showCat(self):
        categories = ''
        for val in self.word_bank.keys():
            categories += val + " "
        return categories

    def wordPicker(self, pick): #Picks a random word from the dictionary based on the category you chose.
        if pick == 'everything':
            pickedCat = random.choice(self.word_bank.keys())
            self.secret_word = random.choice(pickedCat).lower()
            return True
        elif pick in self.word_bank:
            self.secret_word = random.choice(self.word_bank[pick]).lower()
            return True

        else:
            return False






    def menu(self, option):
        if self.state == State.START:
            if option == 'add a new word' or option == 'a':
                self.secret_word = str(input("Enter a Word: ")).lower().strip()
                clear_output()
                self.state = State.LOADING
                return True
            elif option == 'pick list' or option == 'p':
                if self.wordPicker(str(input(self.showCat()).lower())):
                    self.state = State.LOADING
                else:
                    print("Wrong input.")
                    self.menu('pick list')
                return True
            elif option == 'change difficulty' or option == 'd':
                try:
                    self.count = int(input('''How hard do you want the game to be:
Baby = 10
Child = 7
Grown-Up = 5
Master = 3
'''))
                except:
                    print('Error! Try Again!')
                return True
            elif option == 'exit' or option == 'x':
                clear_output()
                retrun False
            else:
                print("Wrong input.")
                return True

    def play(self): # The part of the program that checks where we are in the game and switches us. Looping through after every input.
        if self.state == State.START:
            if self.showStartMenu() == False:
                return
        elif self.state == State.LOADING:
            self.loadWord()
            self.state = State.INGAME
        elif self.state == State.INGAME:

            if self.count <= 0:
                clear_output()
                self.letterListShow()
                print("You Lost!")
                print(f'{self.secret_word} was the word')
                self.showCount()
                self.state = State.LOSTGAME
            elif ''.join(self.word) == self.secret_word:
                clear_output()
                print(f"The word was {self.secret_word}.\nYou Won! with {self.count} guesses to spare!")
                self.state = State.ENDGAME
            elif self.showGameMenu() == False:
                return
        elif self.state == State.ENDGAME or self.state == State.LOSTGAME:
            if self.showEndMenu():
                self.refresh()
        else:
            return
        self.play()

    def showStartMenu(self):
        message = '''
What would you like to do:
* Add a new word: [A]
* Pick list: [P]
* Change Difficulty [D]
* Exit [X]
'''
        user_input = str(input(message)).lower().strip()
        return self.menu(user_input)

    def loadWord(self):
        for i in range(len(self.secret_word)): #creates the blank spaces for the game
            self.word.append('_')

    def showGameMenu(self):
        clear_output()

        self.letterListShow()
        self.showCount()
        self.guess(str(input()).lower().strip())
        return True

    def showEndMenu(self):
        return True

    def letterListShow(self):
        print('\n Possible Letters: ')
        print(*self.possible_letters)
        print('\n Guessed Letters: ')
        print(*self.guessed_letters)
        print(*self.word)

    def guess(self, letter):
        if letter in self.guessed_letters:
            print("Wrong! Try Again!")
        elif letter in self.possible_letters:
            self.possible_letters.remove(letter)
            self.guessed_letters.append(letter)
            if letter not in self.secret_word:
                self.dropCount()

            else:

                for i in range (len(self.secret_word)):
                    if self.secret_word[i] == letter:
                        self.word[i] = letter
        else:
            print(f"{letter} This is not a letter in the Queen's English")

    def dropCount(self): #Drops the count if the answer is wrong
        self.count -= 1

    def showCount(self):  #Displays the current number of lives.
        if self.count <= 0:
            return print('''       _______
         |/      |
         |      (xx)
         |      \|/
         |       |
         |      / \\
         |
        _|___
        ''')
        elif self.count == 1:
             return print('''       _______
         |/      |
         |      (_)
         |      \|/
         |       |
         |      / \\
         |
        _|___
        ''')
        elif self.count == 2:
            return print('''       _______
             |/      |
             |      (_)
             |      \|/
             |       |
             |      /
             |
            _|___
            ''')
        elif self.count == 3:
            return print('''       _______
         |/      |
         |      (_)
         |      \|/
         |       |
         |
         |
        _|___
        ''')
        elif self.count == 4:
            return print('''       _______
         |/      |
         |      (_)
         |      \|/
         |       |
         |
         |
        _|___
        ''')
        elif self.count == 5:
            return print('''       _______
             |/      |
             |      (_)
             |       |
             |       |
             |
             |
            _|___
            ''')
        elif self.count == 6:
            return print('''       _______
         |/      |
         |      (_)
         |
         |
         |
         |
        _|___
        ''')
        elif self.count == 7:
            return print('''       _______
         |/      |
         |
         |
         |
         |
         |
        _|___
        ''')
        else:
            return print('''
             |/
             |
             |
             |
             |
             |
            _|___
            ''')

hangman = Verbum('dictionary.txt')

print(''' _
| |
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __
| '_ \\ / _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                    __/ |
                   |___/                       ''')


hangman.play()
