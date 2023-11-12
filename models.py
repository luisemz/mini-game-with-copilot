import os
import time, datetime
import json


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