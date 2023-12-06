import threading
from queue import Queue

from alisa_gpt_assistant.protocols import SessionDialogProtocol, DialogFactoryProtocol

from .long_text_reader import LongTextReader


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
        continue_trigger: str,
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
        self.continue_trigger = continue_trigger

        self.dialog = None
        self.processing_queue = Queue()
        self.is_processing = False
        self.text_reader = LongTextReader(continue_message)

    def send(
        self, data: SessionDialogProtocol.InputData
    ) -> SessionDialogProtocol.OutputData:
        message = data["message"]
        new_session = data["new_session"]

        if self.text_reader.has_unread_text():
            if message.strip().lower() == self.continue_trigger.lower():
                return {
                    "message": self.text_reader.read_next_part(),
                    "end_session": False,
                }
            else:
                self.text_reader.clear_text()

        if message.strip().lower() == self.stop_trigger.lower():
            return {
                "message": self.goodbye_message,
                "end_session": True,
            }

        if message.strip().lower() in [self.start_trigger.lower(), ""]:
            self.dialog = None
            return {
                "message": self.welcome_message,
                "end_session": False,
            }

        if new_session or self.dialog is None:
            self.dialog = self.dialog_factory.create()

        if not self.is_processing:
            self.is_processing = True
            threading.Thread(target=self._process_message, args=(message,)).start()
            return {
                "message": self.wait_message,
                "end_session": False,
            }

        if self.processing_queue.empty():
            return {
                "message": self.not_ready_message,
                "end_session": False,
            }

        result = self.processing_queue.get_nowait()
        self.is_processing = False

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

    def _process_message(self, message):
        try:
            reply = self.dialog.send(message)
            self.processing_queue.put({"status": "completed", "text": reply})
        except Exception as e:
            self.processing_queue.put({"status": "failed"})
            raise e