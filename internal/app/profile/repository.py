from internal.domain.repository import UserRepository, ShopRepository, ShoppingCartRepository, PaycheckRepository, \
    ProductRepository, ReviewRepository
from internal.domain.model import User, Shop, Product, Paycheck, Review


class ProfileRepository:
    def __init__(self,
                 user_repository: UserRepository,
                 shop_repository: ShopRepository,
                 cart_repository: ShoppingCartRepository,
                 paycheck_repository: PaycheckRepository,
                 product_repository: ProductRepository,
                 review_repository: ReviewRepository):
        self.__user_repository = user_repository
        self.__shop_repository = shop_repository
        self.__cart_repository = cart_repository
        self.__paycheck_repository = paycheck_repository
        self.__product_repository = product_repository
        self.__review_repository = review_repository

    def get_user_profile(self, user_id: int) -> tuple[User, list[Product], list[tuple[Paycheck, list[Product]]], list[Review], tuple[int, float]]:
        print('here!')
        return (self.__user_repository.get_profile_by_id(user_id),
                self.__cart_repository.get_users_products(user_id),
                self.__paycheck_repository.get_users_paychecks(user_id),
                self.__review_repository.get_user_reviews(user_id),
                self.__review_repository.get_user_stats(user_id))

    def get_shop_profile(self, shop_id: int) -> tuple[Shop, list[Product]]:
        return (self.__shop_repository.get_profile_by_id(shop_id),
                self.__product_repository.get_shop_products(shop_id))

    def get_product_profile(self, product_id: int) -> tuple[tuple[Product, str, str], list[Review], tuple[int, float]]:
        return (self.__product_repository.get_product_by_id(product_id),
                self.__review_repository.get_product_reviews(product_id),
                self.__review_repository.get_product_stats(product_id))
