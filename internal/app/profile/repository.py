from internal.domain.repository import UserRepository, ShopRepository
from internal.domain.model import User, Shop


class ProfileRepository:
    def __init__(self, user_repository: UserRepository, shop_repository: ShopRepository):
        self.__user_repository = user_repository
        self.__shop_repository = shop_repository

    def get_user_profile(self, user_id: int) -> User:
        return self.__user_repository.get_profile_by_id(user_id)

    def get_shop_profile(self, shop_id: int) -> Shop:
        return self.__shop_repository.get_profile_by_id(shop_id)
