import jwt

from internal.app.money_operations.repository import MoneyOperationsRepository


class MoneyOperationsUseCase:
    def __init__(self, repository: MoneyOperationsRepository, jwt_secret_key: str):
        self.__repository = repository
        self.__JWT_SECRET_KEY = jwt_secret_key

    def add_money_to_user(self, json_web_token: str, to_add: int):
        decoded = jwt.decode(jwt=json_web_token, key=self.__JWT_SECRET_KEY, options={
                             "verify_signature": False})
        self.__repository.add_money_to_user(decoded['login'], to_add)
