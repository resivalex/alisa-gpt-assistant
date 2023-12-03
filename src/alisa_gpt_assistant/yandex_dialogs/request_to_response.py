from typing import Callable


class RequestToResponse:
    def __init__(self, message_mapper: Callable[[str], str]):
        self.message_mapper = message_mapper

    def map(self, request: dict) -> dict:
        message = request["request"]["original_utterance"]

        reply = self.message_mapper(message)

        return {
            "response": {
                "text": reply,
                "end_session": False,
            },
            "session": request["session"],
            "version": request["version"],
        }
