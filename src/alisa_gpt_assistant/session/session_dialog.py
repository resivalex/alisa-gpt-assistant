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
        check_trigger: str,
        no_request_message: str,
        further_trigger: str,
        further_message: str,
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
        self.check_trigger = check_trigger
        self.no_request_message = no_request_message
        self.further_trigger = further_trigger
        self.further_message = further_message

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
        _new_session = data["new_session"]

        trigger = ""
        if message.strip().lower() in [self.start_trigger.lower(), ""]:
            trigger = "start"
        if message.strip().lower() == self.stop_trigger.lower():
            trigger = "stop"
        if message.strip().lower() == self.check_trigger.lower():
            trigger = "check"
        if message.strip().lower() == self.further_trigger.lower():
            trigger = "further"

        if trigger == "stop":
            self._reset_session()

            return {
                "message": self.goodbye_message,
                "end_session": True,
            }

        if trigger == "start":
            self._reset_session()

            return {
                "message": self.welcome_message,
                "end_session": False,
            }

        if self.message_processing.in_progress():
            return {
                "message": self.not_ready_message,
                "end_session": True,
            }

        if self.message_processing.has_result():
            result = self.message_processing.pop_result()
            text_to_read = result["text"].strip()
            if result["status"] == "failed":
                text_to_read = self.error_message

            self.text_reader.set_text_to_read(text_to_read)

        if trigger == "check":
            if self.text_reader.has_unread_text():
                return {
                    "message": self.text_reader.read_next_part(),
                    "end_session": True,
                }
            else:
                return {
                    "message": self.no_request_message,
                    "end_session": True,
                }

        if trigger == "further":
            return {
                "message": self.further_message,
                "end_session": False,
            }

        if self.dialog is None:
            self.dialog = self.dialog_factory.create()
        self.message_processing.process_message(message, self.dialog.send)
        self.text_reader.clear_text()

        return {
            "message": self.wait_message,
            "end_session": True,
        }
