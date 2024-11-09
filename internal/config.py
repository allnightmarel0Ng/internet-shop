from dotenv import load_dotenv
import os


class Config:
    def __init__(self, postgres_port: str, postgres_db: str, postgres_user: str, postgres_password: str, jwt_secret_key: str, authorization_ws_port: str):
        self.POSTGRES_PORT = postgres_port
        self.POSTGRES_DB = postgres_db
        self.POSTGRES_USER = postgres_user
        self.POSTGRES_PASSWORD = postgres_password
        self.JWT_SECRET_KEY = jwt_secret_key
        self.AUTHORIZATION_WS_PORT = authorization_ws_port


def load_config() -> Config:
    load_dotenv()
    return Config(postgres_port=os.getenv("POSTGRES_PORT"),
                  postgres_db=os.getenv("POSTGRES_DB"),
                  postgres_user=os.getenv("POSTGRES_USER"),
                  postgres_password=os.getenv("POSTGRES_PASSWORD"),
                  jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
                  authorization_ws_port=os.getenv("AUTHORIZATION_WS_PORT"))
