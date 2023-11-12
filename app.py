from random import randint
import os
import time, datetime
import json


class Game:
    def __init__(self):
        self.player = Player()
        self.computer = Computer()
        self.score = Score()
        self.menu()

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


class Player:
    def __init__(self):
        self.name = ""
        self.choice = ""

    def __str__(self):
        return self.name
    

class Computer:
    def __init__(self):
        self.choice = ""

    def convert_choice(self):
        if self.choice == 1:
            return "rock"
        elif self.choice == 2:
            return "paper"
        elif self.choice == 3:
            return "scissors"
        

class Score:
    def __init__(self):
        self.games = 0
        self.wins = 0
        self.loses = 0
        self.ties = 0
        self.result = ""

        self.global_games = 0
        self.global_wins = 0
        self.global_loses = 0
        self.global_ties = 0

    def load_scores(self, player_name):
        if self.games != 0:
            return
        if not os.path.isfile("scores.json"):
            return
        with open("scores.json", "r") as file:
            scores = json.load(file)

        if player_name in scores:
            self.games = scores[player_name]["games"]
            self.wins = scores[player_name]["wins"]
            self.loses = scores[player_name]["loses"]
            self.ties = scores[player_name]["ties"]

        self.global_games = scores["global"]["games"]
        self.global_wins = scores["global"]["wins"]
        self.global_loses = scores["global"]["loses"]
        self.global_ties = scores["global"]["ties"]

    def add_game(self):
        self.games += 1
        self.global_games += 1

    def add_score(self, player, computer_choice):
        self.add_game()
        if player.choice == computer_choice:
            self.ties += 1
            self.global_ties += 1
            self.result = "Tie"
        elif player.choice == "rock" and computer_choice == "scissors":
            self.wins += 1
            self.global_wins += 1
            self.result = "You won!"
        elif player.choice == "paper" and computer_choice == "rock":
            self.wins += 1
            self.global_wins += 1
            self.result = "You won!"
        elif player.choice == "scissors" and computer_choice == "paper":
            self.wins += 1
            self.global_wins += 1
            self.result = "You won!"
        else:
            self.loses += 1
            self.global_loses += 1
            self.result = "You lose!"

    def save_scores(self, player_name):
        if not os.path.isfile("scores.json"):
            scores = {}
        else:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        
        scores["global"] = {
            "games": self.global_games,
            "wins": self.global_wins,
            "loses": self.global_loses,
            "ties": self.global_ties,
        }
        scores[player_name] = {
            "games": self.games,
            "wins": self.wins,
            "loses": self.loses,
            "ties": self.ties,
            "time": time.time(),
        }

        with open("scores.json", "w") as file:
            json.dump(scores, file, indent=4)

    def format_time(self, time):
        return datetime.datetime.fromtimestamp(time).isoformat()\
            .split(".")[0].replace("T", " ").replace("Z", "").replace("-", "/")

    def show_scores(self):
        os.system('clear')
        if not os.path.isfile("scores.json"):
            print("No scores to show!")
            input("Press enter to continue...")
            return
        with open("scores.json", "r") as file:
            scores = json.load(file)
        print("--------------------")
        print("Global score:")
        score = scores["global"]
        print("Games: {} - (Wins: {}/Loses: {}/Ties: {})".format(
            score["games"],
            score["wins"],
            score["loses"],
            score["ties"],
        ))
        print("--------------------")
        print("Score by user:")
        for name, score in scores.items():
            if name == "global":
                continue
            print("Name: {}".format(name))
            print("Games: {} - (Wins: {}/Loses: {}/Ties: {}) - Time: {}".format(
                score["games"],
                score["wins"],
                score["loses"],
                score["ties"],
                self.format_time(score["time"]),
            ))
            print()
    
        print("--------------------")
        input("Press enter to continue...")

if __name__ == "__main__":
    try:
        game = Game()
        game.menu()
    except KeyboardInterrupt:
        print("\nBye!")
        exit()