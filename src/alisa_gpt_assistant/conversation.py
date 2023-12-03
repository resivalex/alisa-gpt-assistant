from typing import TypedDict
import threading

from .open_ai_client import OpenAiClient


class Assistant(TypedDict):
    id: str
    name: str


class Conversation:
    def __init__(
        self,
        client: OpenAiClient,
        assistant_1: Assistant,
        assistant_2: Assistant,
        topic: str,
        message_count: int,
    ):
        self.client = client
        self.assistant_1 = assistant_1
        self.assistant_2 = assistant_2
        self.topic = topic
        self.message_count = message_count

    def start(self):
        thread_1 = self.client.create_thread()
        thread_2 = self.client.create_thread()

        start_message = f"Respond with a starting line to discuss {self.topic}?"
        conversation_thread = threading.Thread(
            target=self._assistant_conversation,
            args=(
                start_message,
                self.assistant_1,
                thread_1.id,
                self.assistant_2,
                thread_2.id,
                self.message_count,
            ),
        )
        conversation_thread.start()
        conversation_thread.join()

    def _assistant_conversation(
        self,
        start_message,
        assistant_a: Assistant,
        thread_a_id,
        assistant_b: Assistant,
        thread_b_id,
        msg_limit: int,
    ):
        message_content = start_message

        for i in range(msg_limit):
            print(f"{i + 1}. {assistant_a['name']}...")

            message_content = self.client.ask_and_get_response(
                assistant_a["id"],
                thread_a_id,
                message_content,
            )
            print(message_content + "\n")

            assistant_a, assistant_b = assistant_b, assistant_a
            thread_a_id, thread_b_id = thread_b_id, thread_a_id
