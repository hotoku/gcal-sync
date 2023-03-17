from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime


class Event(ABC):
    @abstractmethod
    def marked(self) -> bool:
        return NotImplemented

    @abstractproperty
    def id(self) -> str:
        return NotImplemented

    @abstractproperty
    def orig_id(self) -> str:
        return NotImplemented

    @abstractproperty
    def start_time(self) -> datetime:
        return NotImplemented

    @abstractproperty
    def end_time(self) -> datetime:
        return NotImplemented

    @abstractproperty
    def src_name(self) -> str:
        return NotImplemented
