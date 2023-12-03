import time


class AppendingDialog:
    def __init__(self, lag_time: float, append_message: str):
        self.lag_time = lag_time
        self.append_message = append_message

        self.messages = []

    def send(self, message: str) -> str:
        time.sleep(self.lag_time)
        self.messages.append(message)

        return "+".join(self.messages + [self.append_message])


class AppendingDialogFactory:
    def __init__(self, lag_time: float, append_message: str):
        self.lag_time = lag_time
        self.append_message = append_message

    def create(self) -> AppendingDialog:
        return AppendingDialog(
            lag_time=self.lag_time,
            append_message=self.append_message,
        )
