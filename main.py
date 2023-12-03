import os
import dotenv
from fastapi import FastAPI
import uvicorn

from alisa_gpt_assistant.protocols import DialogProtocol
from alisa_gpt_assistant import GptAssistantDialogFactory

dotenv.load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]
assistant_id = os.environ["ASSISTANT_ID"]
webhook_path = os.environ["WEBHOOK_PATH"]
host = os.environ["HOST"]
port = int(os.environ["PORT"])

dialog: DialogProtocol = GptAssistantDialogFactory().create(api_key, assistant_id)

app = FastAPI()


@app.get(webhook_path)
async def webhook(message: str):
    response = dialog.send(message)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
