from alisa_gpt_assistant.protocols import SessionDialogProtocol, DialogFactoryProtocol

from .long_text_reader import LongTextReader
from .background_message_processing import BackgroundMessageProcessing


class SessionDialog(SessionDialogProtocol):
    def __init__(
        self,
        dialog_factory: DialogFactoryProtocol,
        wait_message: str,
        not_ready_message: str,
        error_message: str,
        start_trigger: str,
        welcome_message: str,
        stop_trigger: str,
        goodbye_message: str,
        continue_message: str,
        confirm_trigger: str,
    ):
        self.dialog_factory = dialog_factory
        self.wait_message = wait_message
        self.not_ready_message = not_ready_message
        self.error_message = error_message
        self.start_trigger = start_trigger
        self.welcome_message = welcome_message
        self.stop_trigger = stop_trigger
        self.goodbye_message = goodbye_message
        self.continue_message = continue_message
        self.confirm_trigger = confirm_trigger

        self.dialog = None
        self.text_reader = LongTextReader(continue_message)
        self.message_processing = BackgroundMessageProcessing()

    def _reset_session(self):
        self.dialog = None
        self.text_reader.clear_text()
        self.message_processing.terminate()

    def send(
        self, data: SessionDialogProtocol.InputData
    ) -> SessionDialogProtocol.OutputData:
        message = data["message"]
        new_session = data["new_session"]

        if self.text_reader.has_unread_text():
            if message.strip().lower() == self.confirm_trigger.lower():
                return {
                    "message": self.text_reader.read_next_part(),
                    "end_session": False,
                }
            else:
                self.text_reader.clear_text()

        if message.strip().lower() == self.stop_trigger.lower():
            self._reset_session()

            return {
                "message": self.goodbye_message,
                "end_session": True,
            }

        if message.strip().lower() in [self.start_trigger.lower(), ""]:
            self._reset_session()

            return {
                "message": self.welcome_message,
                "end_session": False,
            }

        if new_session or self.dialog is None:
            self.dialog = self.dialog_factory.create()

        if not self.message_processing.in_progress():
            self.message_processing.process_message(message, self.dialog.send)

        if not self.message_processing.ready():
            return {
                "message": self.wait_message,
                "end_session": False,
            }

        result = self.message_processing.get_result()

        if result["status"] == "failed":
            return {
                "message": self.error_message,
                "end_session": False,
            }

        self.text_reader.set_text_to_read(result["text"].strip())

        return {
            "message": self.text_reader.read_next_part(),
            "end_session": False,
        }
