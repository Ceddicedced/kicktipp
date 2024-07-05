from datetime import datetime
import json
import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import os

from game import Game
from participant import Participant
from state_manager import ChangeInfo


def get_webhook() -> DiscordWebhook:
    if not os.getenv("WEBHOOK_URL"):
        raise Exception("WEBHOOK_URL not set")
    webhook = DiscordWebhook(
        url=os.getenv("WEBHOOK_URL"),  # type: ignore
        username="KickTipp",
        avatar_url="https://www.kicktipp.de/assets/apple-touch-icon.0879fba1.png",
    )
    return webhook


def send_webhook(webhook: DiscordWebhook):
    response = webhook.execute()
    if response.status_code != 200:
        print(f"Failed to send notification: {response.status_code} - {response.text}")


class DiscordNotifier:

    @staticmethod
    def send_notification(message: str):
        webhook = get_webhook()
        webhook.content = message
        send_webhook(webhook)

    @staticmethod
    def send_embed(embed: DiscordEmbed):
        webhook = get_webhook()
        webhook.add_embed(embed)
        send_webhook(webhook)

    @staticmethod
    def send_embeds(embeds: list[DiscordEmbed]):
        webhook = get_webhook()
        for i, embed in enumerate(embeds, 1):
            if i % 10 == 0:
                send_webhook(webhook)
                webhook = get_webhook()
            webhook.add_embed(embed)
        send_webhook(webhook)

    @staticmethod
    def build_participant_message(info: ChangeInfo):
        new: Participant = info.new
        old: Participant = info.old
        message: str = info.message

        def random_choice(key):
            with open("messages.json", "r") as file:
                messages = json.load(file)
            return random.choice(messages[key])

        if new.nr == 1 and old.nr != 1:  # Neuer Erster
            title = "👑👑👑"
            desc = random_choice("neuer_erster")
        elif new.nr == 12 and old.nr != 12:  # Neuer Letzter
            title = "👎👎👎"
            desc = random_choice("neuer_letzter")
        elif new.nr < old.nr:  # Aufstieg
            title = "🎉🎉🎉"
            desc = random_choice("aufstieg").format(old_nr=old.nr)
        elif new.bonus > old.bonus:  # Bonuspunkte
            title = "💰💰💰"
            diff = new.bonus - old.bonus
            desc = random_choice("bonuspunkte").format(diff=diff)
        elif new.win_percent > old.win_percent:  # Neuer Sieg / Richtig getippt
            title = "🔥🔥🔥"
            desc = random_choice("neuer_sieg")

        elif new.total_points > old.total_points:  # Mehr Gesamtpunkte
            title = "🔼🔼🔼"
            diff = new.total_points - old.total_points
            desc = random_choice("mehr_gesamtpunkte").format(diff=diff)
        elif new.total_points < old.total_points:  # Weniger Gesamtpunkte
            title = "🔽🔽🔽"
            diff = old.total_points - new.total_points
            desc = random_choice("weniger_gesamtpunkte").format(diff=diff)
        elif new.nr > old.nr:  # Abstieg
            title = "👎👎👎"
            desc = random_choice("abstieg").format(old_nr=old.nr)
        else:
            title = "🔔🔔🔔"
            desc = "Keine Änderung"
        embed = DiscordEmbed(
            title=title,
            description=f"{desc}",
            color=242424,
        )
        embed.set_author(name=f"{new.pos} - {new.name}")
        embed.set_footer(text=f"Punktzahl: {message}")
        embed.set_timestamp()
        return embed

    @staticmethod
    def build_game_message(info: ChangeInfo):
        new: Game = info.new
        old: Game = info.old
        message = info.message

        title = "⚽⚽⚽"
        team = ""

        if new.result == "0:0" and old.result == "-:-":  # Spielstart
            title = "🔔🔔🔔"
            description = f"{old.home_team} vs {old.away_team} spielt jetzt!"

        elif new.result.endswith("n.V.") and not old.result.endswith(
            "n.V."
        ):  # Verlängerung
            title = "🕒🕒🕒"
            description = "Nachspielzeit! ⏱️"
        elif new.result.endswith("n.E.") and not old.result.endswith(
            "n.E."
        ):  # Elfmeterschießen
            title = "🎯🎯🎯"
            description = "Elfmeterschießen! ⚽"
        elif new.home_score > old.home_score:  # Heimteam hat ein Tor geschossen
            title = "🥅⚽⚽"
            team = old.home_team
            description = f"{team} hat ein Tor geschossen! 🥅\n {message}"
        elif new.away_score > old.away_score:  # Auswärtsteam hat ein Tor geschossen
            title = "⚽⚽🥅"
            team = old.away_team
        elif (
            new.home_score < old.home_score or new.away_score < old.away_score
        ):  # Tor wurde zurückgenommen
            title = "❌❌❌"
            description = f"Tor wurde zurückgenommen! ❌\n {message}"

        embed = DiscordEmbed(
            title=title,
            description=description,
            color=242424,
        )
        embed.set_author(name=f"{old.home_team} vs {old.away_team}")
        embed.set_footer(text=f"Ergebnis: {new.result}")
        start_time = datetime.strptime(new.date_time, "%d.%m.%y %H:%M")
        # Offset by 2 hours
        start_time = start_time.replace(hour=start_time.hour - 2)
        if not start_time:
            start_time = datetime.now()
        embed.set_timestamp(start_time)
        return embed
