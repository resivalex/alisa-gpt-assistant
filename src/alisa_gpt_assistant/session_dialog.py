from alisa_gpt_assistant.protocols import SessionDialogProtocol


class SessionDialog(SessionDialogProtocol):
    def __init__(self, message_mapper):
        self.message_mapper = message_mapper

    def send(
        self, data: SessionDialogProtocol.InputData
    ) -> SessionDialogProtocol.OutputData:
        reply = self.message_mapper(data["message"])

        return {
            "message": reply,
            "end_session": False,
        }
