from dotenv import load_dotenv
import os


class Config:
    def __init__(self, postgres_port: str, postgres_db: str, postgres_user: str, postgres_password: str, jwt_secret_key: str, authorization_ws_port: str):
        self.postgres_port = postgres_port
        self.postgres_db = postgres_db
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.jwt_secret_key = jwt_secret_key
        self.authorization_ws_port = authorization_ws_port


def load_config() -> Config:
    load_dotenv()
    return Config(postgres_port=os.getenv("POSTGRES_PORT"),
                  postgres_db=os.getenv("POSTGRES_DB"),
                  postgres_user=os.getenv("POSTGRES_USER"),
                  postgres_password=os.getenv("POSTGRES_PASSWORD"),
                  jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
                  authorization_ws_port=os.getenv("AUTHORIZATION_WS_PORT"))
