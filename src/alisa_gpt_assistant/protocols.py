from typing import Protocol


class AssistantProtocol(Protocol):
    def speak(self) -> str:
        ...

    def get_id(self) -> str:
        ...
