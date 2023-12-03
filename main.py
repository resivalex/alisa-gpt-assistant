import os
import dotenv

from alisa_gpt_assistant import Conversation, OpenAiClient

dotenv.load_dotenv()


api_key = os.environ["OPENAI_API_KEY"]
assistant_1_id = os.environ["ASSISTANT_1_ID"]
assistant_2_id = os.environ["ASSISTANT_2_ID"]

assistant_1 = {
    "id": assistant_1_id,
    "name": "C",
}
assistant_2 = {
    "id": assistant_2_id,
    "name": "F",
}


client = OpenAiClient(api_key)
conversation = Conversation(client, assistant_1, assistant_2, "rainy day", 5)
conversation.start()
