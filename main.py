import os
import dotenv

from alisa_gpt_assistant import (
    GptAssistantDialogFactory,
    FastApiWebhookProcessor,
    YandexDialogsRequestToResponse,
    SessionDialog,
)

dotenv.load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ASSISTANT_ID = os.environ["ASSISTANT_ID"]

WEBHOOK_PATH = os.environ["WEBHOOK_PATH"]
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])

WAIT_MESSAGE = os.environ["WAIT_MESSAGE"]
NOT_READY_MESSAGE = os.environ["NOT_READY_MESSAGE"]
ERROR_MESSAGE = os.environ["ERROR_MESSAGE"]
START_TRIGGER = os.environ["START_TRIGGER"]
WELCOME_MESSAGE = os.environ["WELCOME_MESSAGE"]
STOP_TRIGGER = os.environ["STOP_TRIGGER"]
GOODBYE_MESSAGE = os.environ["GOODBYE_MESSAGE"]
CONTINUE_MESSAGE = os.environ["CONTINUE_MESSAGE"]
CONTINUE_TRIGGER = os.environ["CONTINUE_TRIGGER"]


dialog_factory = GptAssistantDialogFactory(OPENAI_API_KEY, ASSISTANT_ID)
session_dialog = SessionDialog(
    dialog_factory,
    wait_message=WAIT_MESSAGE,
    not_ready_message=NOT_READY_MESSAGE,
    error_message=ERROR_MESSAGE,
    start_trigger=START_TRIGGER,
    welcome_message=WELCOME_MESSAGE,
    stop_trigger=STOP_TRIGGER,
    goodbye_message=GOODBYE_MESSAGE,
    continue_message=CONTINUE_MESSAGE,
    continue_trigger=CONTINUE_TRIGGER,
)
request_to_response = YandexDialogsRequestToResponse(session_dialog)
webhook_processor = FastApiWebhookProcessor(
    webhook_path=WEBHOOK_PATH,
    host=HOST,
    port=PORT,
    body_mapper=request_to_response.map,
)

if __name__ == "__main__":
    webhook_processor.run()
