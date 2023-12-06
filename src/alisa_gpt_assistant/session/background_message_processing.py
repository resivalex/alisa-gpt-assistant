from typing import TypedDict, Callable
import threading
from queue import Queue


class _MessageProcessingResult(TypedDict):
    status: str
    text: str


class BackgroundMessageProcessing:
    def __init__(self):
        self._processing_queue = Queue()
        self._is_processing = False

    def _process(self, message: str, callback: Callable[[str], str]) -> None:
        try:
            reply = callback(message)
            self._processing_queue.put({"status": "completed", "text": reply})
        except Exception as e:
            self._processing_queue.put({"status": "failed", "text": f"{e}"})
            raise e

    def process_message(self, message, callback: Callable[[str], str]) -> None:
        if self._is_processing:
            raise Exception("Processing is already in progress")
        self._is_processing = True
        threading.Thread(target=self._process, args=(message, callback)).start()

    def in_progress(self) -> bool:
        return self._is_processing

    def ready(self) -> bool:
        return not self._processing_queue.empty()

    def get_result(self) -> _MessageProcessingResult:
        self._is_processing = False
        return self._processing_queue.get_nowait()