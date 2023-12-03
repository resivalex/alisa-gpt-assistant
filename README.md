# Alisa GPT Assistant

OpenAI GPT Assistant integration with Yandex Alisa via dialogs.yandex.ru

## Usage

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
CONTINUE_MESSAGE="Continue?"
CONTINUE_TRIGGER="Yes"
```

_Note: it's recommended to use russian language for triggers._
