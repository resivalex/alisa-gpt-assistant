import time


class ExclamationDialog:
    def __init__(self, lag_time: float):
        self.lag_time = lag_time

        self.messages = []

    def send(self, message: str) -> str:
        time.sleep(self.lag_time)
        self.messages.append(message)

        return "+".join(self.messages) + "!"


class ExclamationDialogFactory:
    def create(self) -> ExclamationDialog:
        return ExclamationDialog(lag_time=10)
