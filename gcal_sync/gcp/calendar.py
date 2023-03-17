from ..calendar import Calendar as BaseCalendar


class Calendar(BaseCalendar):
    def __init__(self, name: str, id: str) -> None:
        self.name = name
        self.id = id

    @classmethod
    def create(cls, name: str, id: str, _: str):
        return cls(name, id)
