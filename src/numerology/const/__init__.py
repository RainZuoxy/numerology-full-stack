from enum import Enum


class BaseParameter(str, Enum):
    @property
    def text(self) -> str:
        return str(self.value)

