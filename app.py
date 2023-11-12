from random import randint
import os

from models import Player, Computer, Score


class Game:
    def __init__(self):
        self.player = Player()
        self.computer = Computer()
        self.score = Score()

    def menu(self):
        while True:
            os.system('clear')
            print("Welcome to Rock, Paper, Scissors game!")
            print("Menu:")
            print("1. Play new game")
            if self.player.name != "":
                print("2. Play again ({})".format(self.player.name))
            else:
                print("2. Play again")
            print("3. View scores")
            print("4. Exit")
            choice = input("Select option: ")
            if choice == "1":
                self.player.name = self.handle_input_name()
                self.play()
            elif choice == "2":
                self.player.name = self.handle_input_name(again=True)
                self.play()
            elif choice == "3":
                self.score.show_scores()
            elif choice == "4":
                print("Bye!")
                exit()
            else:
                print("Select correct option!")

    def handle_input_name(self, forced=False, again=False):
        if again:
            user_name = self.player.name
        elif forced:
            user_name = input("Insert your name: ")
        else:
            if self.player.name != "":
                print("Leave empty to use previous name: {}".format(self.player.name))
            user_name = input("Insert your name: ")
        while user_name == "":
            if self.player.name == "":
                print("You have to insert your name!")
                user_name = input("Insert your name: ")
            else:
                user_name = self.player.name
                break
        return user_name


    def play(self):
        os.system('clear')
        print("Welcome {}!".format(self.player.name))
        print("--------------------")
        
        self.player.choice = input("Choose rock, paper or scissors: ").lower()
        while self.player.choice not in ["rock", "paper", "scissors"]:
            print("You have to choose rock, paper or scissors!")
            self.player.choice = input("Choose rock, paper or scissors: ").lower()
        self.computer.choice = randint(1, 3)
        self.computer.choice = self.computer.convert_choice()
        self.score.load_scores(self.player.name.lower().replace(" ", ""))
        self.score.add_score(self.player, self.computer.choice)
        self.score.save_scores(self.player.name.lower().replace(" ", ""))
        self.show_result()

    def show_result(self):
        os.system('clear')
        print("Game result: {}".format(self.player.name))
        print("--------------------")
        print("Your choice: {}".format(self.player.choice))
        print("Computer choice: {}".format(self.computer.choice))
        print("Result: {}".format(self.score.result))
        print("--------------------")
        input("Press enter to continue...")


if __name__ == "__main__":
    try:
        game = Game()
        game.menu()
    except KeyboardInterrupt:
        print("\nBye!")
        exit()