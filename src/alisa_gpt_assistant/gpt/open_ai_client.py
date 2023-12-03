import openai
import time


class OpenAiClient:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI()
        self.client.api_key = api_key

    def _send_message(self, thread_id, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id, role=role, content=content
        )

    def _run_assistant(self, thread_id, assistant_id):
        return self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )

    def _get_run_status(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id
        )

    def _get_last_assistant_message(self, thread_id):
        messages_response = self.client.beta.threads.messages.list(thread_id=thread_id)
        messages = messages_response.data

        for message in messages:
            if message.role == "assistant":
                assistant_message_content = " ".join(
                    content.text.value
                    for content in message.content
                    if hasattr(content, "text")
                )
                return assistant_message_content.strip()

        return ""  # Return an empty string if there is no assistant message

    def create_thread(self):
        return self.client.beta.threads.create()

    def ask_and_get_response(self, assistant_id, thread_id, message_content) -> str:
        self._send_message(thread_id, "user", message_content)
        run = self._run_assistant(thread_id, assistant_id)

        while True:
            run_status = self._get_run_status(thread_id, run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        return self._get_last_assistant_message(thread_id)
