from typing import Protocol, TypedDict


class DialogProtocol(Protocol):
    def send(self, message: str) -> str:
        ...


class DialogFactoryProtocol(Protocol):
    def create(self) -> DialogProtocol:
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


class DialogProcessorProtocol(Protocol):
    def run(self) -> None:
        ...
