from internal.domain.model import User
from internal.domain.repository import UserRepository, PaycheckRepository, ShoppingCartRepository, ProductRepository

class MoneyOperationsRepository:
    def __init__(self, user_repository: UserRepository, paycheck_repository: PaycheckRepository, shopping_cart_repository: ShoppingCartRepository, product_repository: ProductRepository):
        self.__user_repository = user_repository
        self.__paycheck_repository = paycheck_repository
        self.__shopping_cart_repository = shopping_cart_repository
        self.__product_repository = product_repository
    
    def add_money_to_user(self, login: str, to_add: int):
        self.__user_repository.change_balance(login, to_add)
    
    def buy_shopping_cart(self, user: User):
        # todo: transaction
        user_id = self.__user_repository.get_id_by_login(user.id)
        product_ids = self.__shopping_cart_repository.get_users_products(user_id)
        cart_price = self.__product_repository.get_products_price_sum(product_ids)

        if cart_price > user.balance:
            raise ValueError("not enough money on balance")
        
        self.__paycheck_repository.add_paycheck_for_user(user_id, product_ids)