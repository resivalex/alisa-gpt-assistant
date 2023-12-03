import threading
from queue import Queue
from alisa_gpt_assistant.protocols import SessionDialogProtocol, DialogFactoryProtocol


class SessionDialog(SessionDialogProtocol):
    def __init__(
        self,
        dialog_factory: DialogFactoryProtocol,
        wait_message: str,
        not_ready_message: str,
        error_message: str,
    ):
        self.dialog_factory = dialog_factory
        self.wait_message = wait_message
        self.not_ready_message = not_ready_message
        self.error_message = error_message

        self.dialog = None
        self.processing_queue = Queue()
        self.is_processing = False

    def send(
        self, data: SessionDialogProtocol.InputData
    ) -> SessionDialogProtocol.OutputData:
        if data["new_session"] or self.dialog is None:
            self.dialog = self.dialog_factory.create()

        if not self.is_processing:
            self.is_processing = True
            threading.Thread(
                target=self._process_message, args=(data["message"],)
            ).start()
            return {
                "message": self.wait_message,
                "end_session": False,
            }

        if not self.processing_queue.empty():
            result = self.processing_queue.get_nowait()
            self.is_processing = False

            if result["status"] == "failed":
                return {
                    "message": self.error_message,
                    "end_session": False,
                }

            return {
                "message": result["text"],
                "end_session": False,
            }

        return {
            "message": self.not_ready_message,
            "end_session": False,
        }

    def _process_message(self, message):
        try:
            reply = self.dialog.send(message)
            self.processing_queue.put({"status": "completed", "text": reply})
        except Exception as e:
            self.processing_queue.put({"status": "failed"})
            raise e
