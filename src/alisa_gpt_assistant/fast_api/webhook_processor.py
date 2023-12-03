from typing import Callable
from fastapi import FastAPI, Request
import uvicorn


class WebhookProcessor:
    def __init__(
        self,
        webhook_path: str,
        host: str,
        port: int,
        body_mapper: Callable[[dict], dict],
    ):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.webhook_path = webhook_path
        self.body_mapper = body_mapper

        @self.app.post(self.webhook_path)
        async def webhook(request: Request):
            body = await request.json()

            return self.body_mapper(body)

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)
