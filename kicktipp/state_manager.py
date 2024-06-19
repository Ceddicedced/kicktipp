# state_manager.py

import json
import pickle

from game import Game
from participant import Participant


class StateManager:
    games_file = "games"
    participants_file = "participants"

    def __init__(self, games_file=None, participants_file=None, json=False):
        if games_file:
            self.games_file = games_file
        if participants_file:
            self.participants_file = participants_file
        self.json = json

    def pickle_games(self, games):
        with open(f"{self.games_file}.pkl", "wb") as f:
            pickle.dump(games, f)

    def unpickle_games(self):
        try:
            with open(f"{self.games_file}.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def pickle_participants(self, participants):
        with open(f"{self.participants_file}.pkl", "wb") as f:
            pickle.dump(participants, f)

    def unpickle_participants(self):
        try:
            with open(f"{self.participants_file}.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def games_to_json(self, games):
        with open(f"{self.games_file}.json", "w") as f:
            json.dump([game.__dict__ for game in games], f)

    def participants_to_json(self, participants):
        with open(f"{self.participants_file}.json", "w") as f:
            json.dump([participant.__dict__ for participant in participants], f)

    def json_to_games(self):
        try:
            with open(f"{self.games_file}.json", "r") as f:
                games_json = json.load(f)
            return [Game(**game_json) for game_json in games_json]
        except FileNotFoundError:
            return []

    def json_to_participants(self):
        try:
            with open(f"{self.participants_file}.json", "r") as f:
                participants_json = json.load(f)
            return [
                Participant(**participant_json)
                for participant_json in participants_json
            ]
        except FileNotFoundError:
            return []

    def save_games(self, games):
        if self.json:
            self.games_to_json(games)
        else:
            self.pickle_games(games)

    def restore_games(self):
        if self.json:
            return self.json_to_games()
        else:
            return self.unpickle_games()

    def save_participants(self, participants):
        if self.json:
            self.participants_to_json(participants)
        else:
            self.pickle_participants(participants)

    def restore_participants(self):
        if self.json:
            return self.json_to_participants()
        else:
            return self.unpickle_participants()


class ChangeInfo:

    def __init__(self, old, new, message):
        self.old = old
        self.new = new
        self.message = message

    def __str__(self):
        return f"{self.old} -> {self.new}"


# Could be more efficient with a dictionary
def check_games_changes(new_games, old_games):
    changes = []
    for new_game in new_games:
        for old_game in old_games:
            if new_game == old_game:
                if new_game.result != old_game.result:
                    if old_game.result == "-:-":
                        message = f"{old_game.home_team} vs {old_game.away_team} spielt jetzt!"
                    else:
                        message = f"{old_game.result} -> {new_game.result}"
                    changes.append(ChangeInfo(old_game, new_game, message))
    return changes


def check_participants_changes(new_participants, old_participants):
    changes = []
    for new_participant in new_participants:
        for old_participant in old_participants:
            if new_participant.name == old_participant.name:
                if new_participant != old_participant:
                    changes.append(
                        ChangeInfo(
                            old_participant,
                            new_participant,
                            f"{old_participant.total_points} -> {new_participant.total_points}",
                        )
                    )
    return changes
