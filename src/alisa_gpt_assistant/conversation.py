import time
import threading

from alisa_gpt_assistant.protocols import AssistantProtocol

from .open_ai_client import OpenAiClient


class Conversation:
    def __init__(
        self,
        client: OpenAiClient,
        assistant_1: AssistantProtocol,
        assistant_2: AssistantProtocol,
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
                thread_1,
                self.assistant_2,
                thread_2,
                self.message_count,
            ),
        )
        conversation_thread.start()
        conversation_thread.join()

    def _assistant_conversation(
        self,
        start_message,
        assistant_a: AssistantProtocol,
        thread_a,
        assistant_b: AssistantProtocol,
        thread_b,
        msg_limit: int,
    ):
        message_content = start_message

        for i in range(msg_limit):
            print(assistant_a.speak() + f" (Turn {i + 1})")

            self.client.send_message(thread_a.id, "user", message_content)
            run = self.client.run_assistant(thread_a.id, assistant_a.get_id())

            while True:
                run_status = self.client.get_run_status(thread_a.id, run.id)
                if run_status.status == "completed":
                    break
                time.sleep(1)

            message_content = self.client.get_last_assistant_message(thread_a.id)
            print(message_content + "\n")

            assistant_a, assistant_b = assistant_b, assistant_a
            thread_a, thread_b = thread_b, thread_a
