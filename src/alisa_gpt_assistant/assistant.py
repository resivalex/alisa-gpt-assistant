class Assistant:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def speak(self) -> str:
        return f"\033[94m\033[1m{self.name} speaking...\033[0m"

    def get_id(self) -> str:
        return self.id
