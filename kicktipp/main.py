# main.py

import os
import time
from dotenv import load_dotenv
from fetcher import Fetcher, Parser
from notifier import DiscordNotifier
from state_manager import (
    ChangeInfo,
    StateManager,
    check_games_changes,
    check_participants_changes,
)

VERSION = "0.1.2"

# Load environment variables from .env file
load_dotenv()

# Get URL and WEBHOOK_URL from environment variables
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


class MainApplication:
    def __init__(self, url, state_manager):
        self.url = url
        self.state_manager = state_manager

    def fetch_and_parse(self):
        html_content = Fetcher.fetch_html_content(self.url)
        games = Parser.parse_games(html_content)
        participants = Parser.parse_participants(html_content)
        return games, participants

    def first_run(self):
        print(VERSION)
        games, participants = self.fetch_and_parse()
        for game in games:
            print(game)

        print("\nParticipants:")
        print("Pos\tName\tDay\tBonus\tSiege\tTotal Points")
        for participant in participants:
            print(participant)

    def run(self):
        while True:
            try:
                # Fetch and parse games and participants
                games, participants = self.fetch_and_parse()
                notifier = DiscordNotifier()
                embeds = []

                # Compare current games with stored games
                # stored_games = self.state_manager.restore_games()
                stored_games = self.state_manager.restore_games()
                game_changes = check_games_changes(games, stored_games)
                if game_changes:
                    for change_info in game_changes:
                        print(f"Game Change: {change_info}")
                        embed = notifier.build_game_message(change_info)
                        embeds.append(embed)
                # self.state_manager.save_games(games)
                self.state_manager.save_games(games)

                # Compare current participants with stored participants
                # stored_participants = self.state_manager.restore_participants()
                stored_participants = self.state_manager.restore_participants()
                participant_changes: list[ChangeInfo] = check_participants_changes(
                    participants, stored_participants
                )
                if participant_changes:
                    for change_info in participant_changes:
                        print(f"Participant Change: {change_info}")
                        embed = notifier.build_participant_message(change_info)
                        embeds.append(embed)
                # self.state_manager.save_participants(participants)
                self.state_manager.save_participants(participants)

                # Send notifications
                if embeds:
                    notifier.send_embeds(embeds)
            except Exception as e:
                print(f"Error: {e}")

            # Wait for some seconds before checking again
            try:
                time.sleep(30)
            except KeyboardInterrupt:
                print("Exiting...")
                break


if __name__ == "__main__":
    state_manager = StateManager(json=True)
    app = MainApplication(URL, state_manager)
    app.first_run()
    app.run()
