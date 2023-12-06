import time

from alisa_gpt_assistant.protocols import SessionDialogProtocol


class CountingDialog:
    def __init__(self, lag_time: float, append_to_response: str = "!") -> None:
        self.lag_time = lag_time
        self.append_to_response = append_to_response

        self.messages = []

    def send(self, message: str) -> str:
        time.sleep(self.lag_time)
        self.messages.append(message)

        return f"{len(self.messages)}. {message}{self.append_to_response}"


class CountingDialogFactory:
    def __init__(self, lag_time: float, append_to_response: str):
        self.lag_time = lag_time
        self.append_to_response = append_to_response

    def create(self) -> CountingDialog:
        return CountingDialog(
            lag_time=self.lag_time,
            append_to_response=self.append_to_response,
        )


class ConsoleProcessor:
    def __init__(
        self, session_dialog: SessionDialogProtocol, exit_trigger: str = "exit"
    ) -> None:
        self.session_dialog = session_dialog
        self.exit_trigger = exit_trigger

    def run(self) -> None:
        print(f'Enter "{self.exit_trigger}" to exit.')
        new_session = True
        while True:
            message = input("You: ")
            if message == self.exit_trigger:
                break

            input_data = {
                "message": message,
                "new_session": new_session,
            }
            output_data = self.session_dialog.send(input_data)
            print(f"Bot: {output_data['message']}")

            if output_data["end_session"]:
                print("Session ended.")
                new_session = True
                continue

            new_session = False
