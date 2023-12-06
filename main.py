import os
import dotenv
import sys

sys.path.append("./src")

from alisa_gpt_assistant import (
    GptAssistantDialogFactory,
    FastApiWebhookProcessor,
    YandexDialogsRequestToResponse,
    SessionDialog,
)
from alisa_gpt_assistant.protocols import DialogProcessorProtocol, DialogFactoryProtocol
from alisa_gpt_assistant.stubs import CountingDialogFactory, ConsoleProcessor

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


def create_session_dialog(dialog_factory: DialogFactoryProtocol) -> SessionDialog:
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

    return session_dialog


def setup_yandex_dialogs_processor() -> DialogProcessorProtocol:
    dialog_factory = GptAssistantDialogFactory(OPENAI_API_KEY, ASSISTANT_ID)
    session_dialog = create_session_dialog(dialog_factory)
    request_to_response = YandexDialogsRequestToResponse(session_dialog)
    webhook_processor = FastApiWebhookProcessor(
        webhook_path=WEBHOOK_PATH,
        host=HOST,
        port=PORT,
        body_mapper=request_to_response.map,
    )

    return webhook_processor


def setup_console_processor() -> DialogProcessorProtocol:
    dialog_factory = CountingDialogFactory(lag_time=5, append_to_response="!")
    session_dialog = create_session_dialog(dialog_factory)
    console_processor = ConsoleProcessor(session_dialog)

    return console_processor


def setup_dialog_processor(debug=False) -> DialogProcessorProtocol:
    if debug:
        return setup_console_processor()

    return setup_yandex_dialogs_processor()


if __name__ == "__main__":
    dialog_processor = setup_dialog_processor()
    dialog_processor.run()
