class Game:
    def __init__(self, date_time, home_team, away_team, group, result):
        self.date_time: str = date_time
        self.home_team: str = home_team
        self.away_team: str = away_team
        self.group: str = group
        self.result: str = result

    @property
    def id(self):
        return f"{self.date_time}-{self.home_team}-{self.away_team}-{self.group}"

    @property
    def home_score(self):
        if self.result == "-:-":
            return 0
        return int(self.result.split(":")[0])

    @property
    def away_score(self):
        if self.result == "-:-":
            return 0
        return int(self.result.split(":")[1])

    def __str__(self):
        return f"{self.date_time}:\t {self.home_team} vs {self.away_team} ({self.group}) - Result: {self.result}"

    def __eq__(self, other):
        return isinstance(other, Game) and self.id == other.id

    def __repr__(self):
        return f"Game(date_time={self.date_time}, home_team={self.home_team}, away_team={self.away_team}, group={self.group}, result={self.result})"

    def __getstate__(self):
        return {
            "date_time": self.date_time,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "group": self.group,
            "result": self.result,
        }

    def __setstate__(self, state):
        self.date_time = state["date_time"]
        self.home_team = state["home_team"]
        self.away_team = state["away_team"]
        self.group = state["group"]
        self.result = state["result"]

    def to_json(self):
        return {
            "date_time": self.date_time,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "group": self.group,
            "result": self.result,
        }

    @classmethod
    def from_row(cls, row):
        cells = row.find_all("td")
        if cells:
            date_time = cells[0].text.strip()
            home_team = cells[1].text.strip()
            away_team = cells[2].text.strip()
            group = cells[3].text.strip() if len(cells) > 3 else None
            result = cells[4].text.strip() if len(cells) > 4 else cells[3].text.strip()
            return cls(date_time, home_team, away_team, group, result)
        else:
            raise ValueError("Invalid row format for Game parsing")
