# 🤖 Alisa GPT Assistant

Integration of OpenAI's GPT Assistant with Yandex Alisa via dialogs.yandex.ru.

## 📖 Usage

### 🚀 Triggers

Utilize Alisa scenarios to activate these triggers:

- **🌟 Start**: Begins a new session. The assistant sends a welcome message, signaling readiness.
- **🔍 Check**: Dual purpose:
   1. Awaiting a response? This prompts an update.
   2. Long response? This continues the reading.
- **➡️ Further**: Continues the dialogue, maintaining context for in-depth conversations.

> 💡 _Tip: Use Russian for trigger commands. Configurable._

### 🗨️ Conversation Example

- **You**: "Start"
- **Alisa**: "I'm ready."
- **You**: "Tell a long story about the ocean."
- **You**: "Check"
- **Alisa**: "Not ready yet."
- **You**: "Check"
- **Alisa**: "Once upon a time the Ocean... Can't read whole message. Check again."
- **You**: "Check"
- **Alisa**: "...and so the Ocean... That's all."
- **You**: "Further"
- **Alisa**: "*Ask a follow-up question.*"
- **You**: "What's the main substance it contains?"
- **Alisa**: "Water."

## 🚀 Launch

Place a configured .env file in the project root and run the following in your terminal:

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
