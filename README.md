# KickTipp to Discord Notifications

This script sends notifications to a Discord channel when a new event ocurs on a tipping tournament on KickTipp.

## Installation

1. Clone this repository
2. Install the requirements with `poetry install`
3. Create a `.env` file with the following content:
```
WEBHOOK_URL=<your_discord_webhook_url>
URL=<the_kicktipp_tournament_url>
```
4. Run the script with `poetry run python main.py`



