from alisa_gpt_assistant.protocols import SessionDialogProtocol


class RequestToResponse:
    def __init__(self, session_dialog: SessionDialogProtocol):
        self.session_dialog = session_dialog

    def map(self, request: dict) -> dict:
        message = request["request"]["original_utterance"]
        new_session = request["session"]["new"]

        reply = self.session_dialog.send(
            {
                "message": message,
                "new_session": new_session,
            }
        )

        return {
            "response": {
                "text": reply["message"],
                "end_session": reply["end_session"],
            },
            "session": request["session"],
            "version": request["version"],
        }
