class User:
    def __init__(self, name: str, login: str):
        self.name = name
        self.login = login

    def to_dict(self) -> dict:
        return {"name": self.name, "login": self.login}
