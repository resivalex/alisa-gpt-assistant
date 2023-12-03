from typing import Callable, List
from fastapi import FastAPI
import uvicorn


class MessageSource:
    def __init__(self, webhook_path: str, host: str, port: int):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.webhook_path = webhook_path
        self.callback = None

        @self.app.get(self.webhook_path)
        async def webhook(message: str):
            if not self.callback:
                raise Exception("No callback function registered")

            return {"response": self.callback(message)}

    def register(self, callback: Callable[[str], str]):
        self.callback = callback

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)
