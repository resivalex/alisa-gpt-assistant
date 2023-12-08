# Alisa GPT Assistant

OpenAI GPT Assistant integration with Yandex Alisa via dialogs.yandex.ru

## Usage

### Triggers

- **Start**: Initiates a new session with the assistant. The assistant acknowledges with a welcome message, indicating readiness to engage.
- **Check**: Serves two purposes: 
   1. If the assistant's response is being processed or awaited, this command prompts the assistant to provide an update or the next part of the response.
   2. If the assistant's response is too lengthy for one message, "Check" continues the reading of the remaining text.
- **Further**: Used to continue the dialogue with the GPT Assistant, keeping the context of previous messages intact. This command is essential for extended conversations and deeper exploration of topics.

### Conversation Example

- **User**: *Start*
- **Alisa**: I'm ready.
- **User**: Tell a long story about the ocean.
- **User**: *Check*
- **Alisa**: Not ready yet.
- **User**: *Check*
- **Alisa**: Once upon a time the Ocean ... Can't read whole message. Check again.
- **User**: *Check*
- **Alisa**: ...and so the Ocean ... That's it.
- **User**: *Further*
- **Alisa**: Ask a follow-up question.
- **User**: What's the main substance it contains?
- **Alisa**: Water.

## Launch

```bash
docker-compose up --build
```

## Configuration

.env
```
OPENAI_API_KEY=sk-...
ASSISTANT_ID=asst_...

WEBHOOK_PATH=/webhook
HOST=0.0.0.0
PORT=3000

WAIT_MESSAGE="Wait please."
NOT_READY_MESSAGE="Not ready yet."
ERROR_MESSAGE="Error happened."
START_TRIGGER="Start"
WELCOME_MESSAGE="I'm ready."
STOP_TRIGGER="Stop"
GOODBYE_MESSAGE="Goodbye."
CONTINUE_MESSAGE="Can't read whole message. Check again."
CHECK_TRIGGER="Check"
NO_REQUEST_MESSAGE="No request."
FURTHER_TRIGGER="Further"
FURTHER_MESSAGE="Ask a follow up question."
```

_Note: it's recommended to use russian language for triggers._
