from dataclasses import dataclass


@dataclass
class Calendar:
    name: str
    id: str

    @classmethod
    def parse(cls, s: str) -> "Calendar":
        ss = s.split(":")
        assert len(ss) == 2, f"invalid format: {s}"
        return cls(*ss)
