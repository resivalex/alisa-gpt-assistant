from alisa_gpt_assistant.protocols import DialogProtocol

from .open_ai_client import OpenAiClient
from .assistant_dialog import AssistantDialog


class AssistantDialogFactory:
    def create(self, open_api_key: str, assistant_id: str) -> DialogProtocol:
        client = OpenAiClient(open_api_key)
        thread = client.create_thread()

        return AssistantDialog(client, assistant_id, thread.id)
