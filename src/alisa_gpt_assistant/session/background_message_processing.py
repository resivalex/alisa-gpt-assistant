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
        self._current_thread_order_number = 0

    def _process(
        self, message: str, callback: Callable[[str], str], thread_order_number: int
    ) -> None:
        try:
            reply = callback(message)
            if thread_order_number == self._current_thread_order_number:
                self._is_processing = False
                self._processing_queue.put({"status": "completed", "text": reply})
        except Exception as e:
            if thread_order_number == self._current_thread_order_number:
                self._is_processing = False
                self._processing_queue.put({"status": "failed", "text": f"{e}"})
            raise e

    def process_message(self, message, callback: Callable[[str], str]) -> None:
        if self._is_processing:
            raise Exception("Processing is already in progress")
        self._is_processing = True
        self._current_thread_order_number += 1
        if not self._processing_queue.empty():
            self._processing_queue.get_nowait()
        threading.Thread(
            target=self._process,
            args=(message, callback, self._current_thread_order_number),
        ).start()

    def terminate(self) -> None:
        self._is_processing = False
        self._current_thread_order_number += 1

    def in_progress(self) -> bool:
        return self._is_processing

    def has_result(self) -> bool:
        return not self._processing_queue.empty()

    def get_result(self) -> _MessageProcessingResult:
        if self._is_processing:
            raise Exception("Processing is in progress")
        if not self.has_result():
            raise Exception("No result")

        return self._processing_queue.get_nowait()
