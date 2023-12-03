import os
import dotenv

from alisa_gpt_assistant.protocols import DialogProtocol
from alisa_gpt_assistant import GptAssistantDialogFactory

dotenv.load_dotenv()


api_key = os.environ["OPENAI_API_KEY"]
assistant_id = os.environ["ASSISTANT_ID"]

dialog: DialogProtocol = GptAssistantDialogFactory().create(api_key, assistant_id)


while True:
    message = input("You: ")
    response = dialog.send(message)
    print(f"Bot: {response}")
