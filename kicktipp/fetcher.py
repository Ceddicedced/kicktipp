from bs4 import BeautifulSoup
import requests

from game import Game
from participant import Participant


class Fetcher:
    @staticmethod
    def fetch_html_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(
                f"Failed to fetch the page, status code: {response.status_code}"
            )


class Parser:
    @staticmethod
    def parse_games(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        rows = soup.select("tr.clickable")
        games = []
        for row in rows:
            if "data-teilnehmer-id" not in row.attrs:
                games.append(Game.from_row(row))
        return games

    @staticmethod
    def parse_participants(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        rows = soup.select("tr.clickable")
        participants = []
        for row in rows:
            if "data-teilnehmer-id" in row.attrs:
                participants.append(Participant.from_row(row))
        return participants
