import os
import dotenv

from alisa_gpt_assistant.protocols import DialogProtocol, MessageSourceProtocol
from alisa_gpt_assistant import GptAssistantDialogFactory, FastApiMessageSource

dotenv.load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ASSISTANT_ID = os.environ["ASSISTANT_ID"]
WEBHOOK_PATH = os.environ["WEBHOOK_PATH"]
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])


dialog: DialogProtocol = GptAssistantDialogFactory().create(
    OPENAI_API_KEY, ASSISTANT_ID
)


def connect_dialog_to_source(dialog: DialogProtocol, source: MessageSourceProtocol):
    def process_message(message: str) -> str:
        return dialog.send(message)

    source.register(process_message)


fast_api_source = FastApiMessageSource(WEBHOOK_PATH, HOST, PORT)

if __name__ == "__main__":
    connect_dialog_to_source(dialog, fast_api_source)
    fast_api_source.run()
