I'll add a note about the convenience of using Alisa scenarios to call triggers and update the style of the dialogue in the "Conversation Example" section as per your request. Here's the revised README:

---

# Alisa GPT Assistant

OpenAI GPT Assistant integration with Yandex Alisa via dialogs.yandex.ru

## Usage

### Triggers

It's convenient to use Alisa scenarios to call these triggers:

- **Start**: Initiates a new session with the assistant. The assistant acknowledges with a welcome message, indicating readiness to engage.
- **Check**: Serves two purposes: 
   1. If the assistant's response is being processed or awaited, this command prompts the assistant to provide an update or the next part of the response.
   2. If the assistant's response is too lengthy for one message, "Check" continues the reading of the remaining text.
- **Further**: Used to continue the dialogue with the GPT Assistant, keeping the context of previous messages intact. This command is essential for extended conversations and deeper exploration of topics.

_Note: It's recommended to use Russian language for triggers. You can configure them._

### Conversation Example

- You: **Start**
- Alisa: *I'm ready.*
- You: Tell a long story about the ocean.
- You: **Check**
- Alisa: *Not ready yet.*
- You: **Check**
- Alisa: *Once upon a time the Ocean ... Can't read whole message. Check again.*
- You: **Check**
- Alisa: *...and so the Ocean ... That's it.*
- You: **Further**
- Alisa: *Ask a follow-up question.*
- You: What's the main substance it contains?
- Alisa: *Water.*

## Launch

```bash
docker-compose up --build
```

## Configuration

[ENG example](./.env.en.example) / [RUS example](./.env.ru.example)

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
