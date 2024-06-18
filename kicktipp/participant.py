class Participant:
    def __init__(self, pos, name, day, bonus, win_percent, total_points):
        self.pos: str = pos
        self.name: str = name

        self.day: int = self._to_int(day)
        self.bonus: int = self._to_int(day)
        self.win_percent: int = self._to_int(day)
        self.total_points: int = self._to_int(day)

    def _to_int(self, value):
        if value == "-" or value == "":
            return 0
        return int(value)

    def __str__(self):
        return f"{self.pos}\t{self.name}\t{self.day}\t{self.bonus}\t{self.win_percent}\t{self.total_points}"

    def __setstate__(self, state):
        self.pos = state["pos"]
        self.name = state["name"]
        self.day = state["day"]
        self.bonus = state["bonus"]
        self.win_percent = state["win_percent"]
        self.total_points = state["total_points"]

    def __getstate__(self):
        return {
            "pos": self.pos,
            "name": self.name,
            "day": self.day,
            "bonus": self.bonus,
            "win_percent": self.win_percent,
            "total_points": self.total_points,
        }

    def __eq__(self, other):
        return isinstance(other, Participant) and self.name == other.name

    def __repr__(self) -> str:
        return f"Participant(pos={self.pos}, name={self.name}, day={self.day}, bonus={self.bonus}, win_percent={self.win_percent}, total_points={self.total_points})"

    @classmethod
    def from_row(cls, row):
        cells = row.select("td")
        pos = cells[0].text.strip()
        name = row.select_one(".mg_name").text.strip()
        day = cells[-4].text.strip()
        bonus = cells[-3].text.strip()
        win_percent = cells[-2].text.strip()
        total_points = cells[-1].text.strip()
        return cls(pos, name, day, bonus, win_percent, total_points)

    @property
    def nr(self):
        return int(self.pos.replace(".", ""))
