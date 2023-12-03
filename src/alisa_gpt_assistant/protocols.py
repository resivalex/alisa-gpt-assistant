from typing import Protocol, Callable


class DialogProtocol(Protocol):
    def send(self, message: str) -> str:
        ...


class MessageSourceProtocol(Protocol):
    def register(self, callback: Callable[[str], str]):
        ...
