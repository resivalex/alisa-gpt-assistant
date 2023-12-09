# 🔊 Alisa GPT Assistant

Integration of OpenAI's GPT Assistant with Yandex Alisa via dialogs.yandex.ru.

## 📋 How to Use

### Key Triggers

- **✨ Start**: Initiates a new session.
- **👀 Check**: Serves a dual role:
   1. Awaiting a response? This prompts an update.
   2. Long response? This continues the reading.
- **👣️ Further**: Continues the dialogue, maintaining context for in-depth conversations.

> 💡 _Tip: Triggers are best used in Russian but are fully customizable. Alisa "scenarios" enhance user experience._

### 💬 Example Conversation

- **You**: "Start"
- **Alisa**: "I'm ready."
- **You**: "Tell a long story about the ocean."
- **You**: "Check"
- **Alisa**: "Not ready yet."
- **You**: "Check"
- **Alisa**: "Once upon a time the Ocean... Need more? Check again."
- **You**: "Check"
- **Alisa**: "...and so the Ocean... That's all."
- **You**: "Further"
- **Alisa**: "What would you like to know next?"
- **You**: "What's the main component?"
- **Alisa**: "Primarily, it's water."

## 🚀 Getting Started

Ensure a `.env` file with the necessary configurations is placed in the project root. This file should include API keys and webhook settings. To launch, execute:

```bash
docker-compose up --build
```

## ⚙️ Configuration

See examples of the `.env` file:
  - [ENG example](./.env.en.example)
  - [RUS example](./.env.ru.example)
