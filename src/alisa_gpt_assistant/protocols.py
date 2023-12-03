from typing import Protocol, TypedDict


class DialogProtocol(Protocol):
    def send(self, message: str) -> str:
        ...


class SessionDialogProtocol(Protocol):
    class InputData(TypedDict):
        message: str
        new_session: bool

    class OutputData(TypedDict):
        message: str
        end_session: bool

    def send(self, data: InputData) -> OutputData:
        ...
