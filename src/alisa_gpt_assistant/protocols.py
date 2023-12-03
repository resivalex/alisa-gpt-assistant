from typing import Protocol


class DialogProtocol(Protocol):
    def send(self, message: str) -> str:
        ...
