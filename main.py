import os
import dotenv

from alisa_gpt_assistant import (
    GptAssistantDialogFactory,
    FastApiWebhookProcessor,
    YandexDialogsRequestToResponse,
    SessionDialog,
)

# from alisa_gpt_assistant.stubs import ExclamationDialog

dotenv.load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ASSISTANT_ID = os.environ["ASSISTANT_ID"]

WEBHOOK_PATH = os.environ["WEBHOOK_PATH"]
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])


dialog = GptAssistantDialogFactory().create(OPENAI_API_KEY, ASSISTANT_ID)
# dialog = ExclamationDialog()
session_dialog = SessionDialog(dialog.send)
request_to_response = YandexDialogsRequestToResponse(session_dialog)
webhook_processor = FastApiWebhookProcessor(
    webhook_path=WEBHOOK_PATH,
    host=HOST,
    port=PORT,
    body_mapper=request_to_response.map,
)

if __name__ == "__main__":
    webhook_processor.run()
