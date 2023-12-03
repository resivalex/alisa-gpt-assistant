import openai


class OpenAiClient:
    def __init__(self, api_key):
        self.client = openai.OpenAI()
        self.client.api_key = api_key

    def create_assistant(self, params):
        return self.client.beta.assistants.create(**params)

    def create_thread(self):
        return self.client.beta.threads.create()

    def send_message(self, thread_id, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id, role=role, content=content
        )

    def run_assistant(self, thread_id, assistant_id):
        return self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )

    def get_run_status(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id
        )

    def get_last_assistant_message(self, thread_id):
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
