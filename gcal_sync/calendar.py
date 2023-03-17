from __future__ import annotations
from abc import ABC, abstractclassmethod


class Calendar(ABC):
    @abstractclassmethod
    def create(cls, name: str, id: str, provider: str):
        return NotImplemented
