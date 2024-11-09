from internal.domain.model import Shop, User
from internal.domain.repository import ShopRepository, UserRepository


class AuthorizationRepository:
    def __init__(self, shop_repository: ShopRepository, user_repository: UserRepository):
        self.__shop_repository = shop_repository
        self.__user_repository = user_repository

    def authorize_shop(self, login: str, password: str) -> Shop:
        return self.__shop_repository.authorize_shop(login, password)

    def authorize_user(self, login: str, password: str) -> User:
        return self.__user_repository.authorize_user(login, password)
