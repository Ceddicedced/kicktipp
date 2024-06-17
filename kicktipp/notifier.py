from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import os

from game import Game
from participant import Participant
from state_manager import ChangeInfo


def get_webhook() -> DiscordWebhook:
    webhook = DiscordWebhook(
        url=os.getenv("WEBHOOK_URL"),
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

        if new.nr == 1 and old.nr != 1:
            title = "👑👑👑"
            info = "Neuer Erster!"
        elif new.nr == 12 and old.nr != 12:
            title = "👎👎👎"
            info = "Dabei sein ist alles!"
        elif new.win_percent > old.win_percent:
            title = "🔥🔥🔥"
            info = "Da brennt die Luft! Was ein Tipper!"
        elif new.nr < old.nr:
            title = "🎉🎉🎉"
            info = "Aufstieg vom {old.nr} Platz!"
        elif new.bonus > old.bonus:
            title = "💰💰💰"
            diff = new.bonus - old.bonus
            info = "Bonuspunkte! +{diff} Punkte!"
        elif new.total_points > old.total_points:
            title = "🔼🔼🔼"
            diff = new.total_points - old.total_points
            info = "Es gibt Puuuunkte! +{diff} Punkte!"
        elif new.total_points < old.total_points:
            title = "🔽🔽🔽"
            diff = old.total_points - new.total_points
            info = "Das war wohl nix! -{diff} Punkte!"
        else:
            title = "🔔🔔🔔"

        embed = DiscordEmbed(
            title=title,
            description=f"{info}",
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

        if new.result == "0:0" and old.result == "-:-":  # Spielstart
            title = "🔔🔔🔔"
            description = f"{old.home_team} vs {old.away_team} spielt jetzt!"
        else:
            title = "⚽⚽⚽"
            team = ""
            if new.home_score > old.home_score:  # Heimteam hat ein Tor geschossen
                title = "🥅⚽⚽"
                team = old.home_team
            elif new.away_score > old.away_score:  # Auswärtsteam hat ein Tor geschossen
                title = "⚽⚽🥅"
                team = old.away_team

            description = f"{team} hat ein Tor geschossen! 🥅\n {message}"

            if (
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
        # 18.06.24 21:00 to datetime
        start_time = datetime.strptime(new.date_time, "%d.%m.%y %H:%M")
        # Offset by 2 hours
        start_time = start_time.replace(hour=start_time.hour - 2)
        if not start_time:
            start_time = datetime.now()
        embed.set_timestamp(start_time)
        return embed
