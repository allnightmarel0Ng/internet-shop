from internal.infrastructure.postgres import Database
from internal.domain.model import *


class UserRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__AUTHORIZATION_SQL = """
            SELECT u.id, c.password_hash
            FROM public.users
            JOIN public.user_credentials AS c ON c.user_id = u.id 
            WHERE login = :login;
            """
        self.__CHANGE_BALANCE_SQL = """
            UPDATE public.users
            SET balance = balance + :diff
            WHERE id = :user_id;
            """
        self.__GET_PROFILE_BY_ID_SQL = """
            SELECT
                id,
                name,
                login,
                balance
            FROM public.users
            WHERE id = :id
            """

    def __map_to_user(self, query_result) -> User:
        return User(user_id=query_result['id'], name=query_result['name'], login=query_result['login'], balance=query_result['balance'])

    def authorize_user(self, login: str) -> tuple[int, str]:
        result = self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login}
        )
        return result['id'], result['password_hash']

    def change_balance(self, user_id: int, diff: int):
        print(self.__db.execute(
            self.__CHANGE_BALANCE_SQL,
            {"diff": diff, "user_id": user_id}))

    def get_profile_by_id(self, user_id: int) -> User:
        result = self.__db.query_row(
            self.__GET_PROFILE_BY_ID_SQL,
            {"id": user_id})
        return self.__map_to_user(result)


class ShopRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__AUTHORIZATION_SQL = """
            SELECT u.id, c.password_hash
            FROM public.shops
            JOIN public.shop_credentials AS c ON c.shop_id = u.id
            WHERE login = :login;
            """
        self.__GET_PROFILE_BY_ID_SQL = """
            SELECT
                id,
                name,
                login
            FROM public.shops
            WHERE id = :id;
            """

    def __map_to_shop(self, query_result) -> Shop:
        return Shop(shop_id=query_result['id'], name=query_result['name'], login=query_result['login'])

    def authorize_shop(self, login: str) -> tuple[int, str]:
        result = self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login}
        )
        return result['id'], result['password_hash']

    def get_profile_by_id(self, shop_id: int) -> Shop:
        result = self.__db.query_row(
            self.__GET_PROFILE_BY_ID_SQL,
            {'id': shop_id})
        return self.__map_to_shop(result)


class CategoryRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__GET_BY_ID_SQL = """
            SELECT id, name 
            FROM public.categories 
            WHERE id = :id;
            """

    def __map_to_category(self, query_result) -> Category:
        return Category(category_id=query_result[0], name=query_result[1])

    def get_category_by_id(self, category_id: int) -> Category:
        return self.__map_to_category(self.__db.query_row(
            self.__GET_BY_ID_SQL, {"id": id}
        ))


class ProductRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__GET_BY_ID_SQL = """
            SELECT
                c.name,
                s.name,
                s.login,
                p.name,
                p.price,
                p.description
            FROM public.products AS p
            JOIN public.categories AS c ON c.id = p.category_id
            JOIN public.shops AS s ON s.id = p.shop_id
            WHERE p.id = :id;
            """
        self.__GET_SUM_PRICE_BY_IDS_SQL = """
            SELECT SUM(price) AS price
            FROM public.products
            WHERE id IN
            """


class PaycheckRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__GET_PAYCHECKS_BY_USER_ID = """
            SELECT
                pa.id AS paycheck_id,
                u.name AS user_name,
                u.login AS user_login,
                u.balance AS user_balance,
                c.name AS category_name,
                s.name AS shop_name,
                s.login AS shop_login,
                p.name AS product_name,
                p.price AS product_price,
                p.description AS product_description,
            FROM public.paychecks AS pa
            JOIN public.users AS u ON u.id = pa.user_id
            JOIN public.products AS p ON p.id = pa.product_id
            JOIN public.categories AS c ON c.id = p.category_id
            JOIN public.shops AS s ON s.id = p.shop_id
            WHERE u.id = :id
            ORDER BY pa.id;
            """
        self.__ADD_PAYCHECK_SQL = """
            INSERT INTO public.paychecks (paycheck_id, user_id, product_id)
            VALUES 
            """

        self.__ADD_PAYCHECK_VALUE_TEMPLATE_SQL = "(COALESCE(MAX(paycheck_id), 0) + 1, {user_id}, {product_id})"


class ShoppingCartRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__ADD_PRODUCT_TO_CART_SQL = """
            INSERT INTO public.shopping_carts (user_id, product_id)
            VALUES (:user_id, :product_id);
            """
        self.__DROP_PRODUCT_FROM_USERS_CART_SQL = """
            DELETE FROM public.shopping_carts
            WHERE user_id = :user_id AND product_id = :product_id;
            """
        self.__GET_USERS_PRODUCTS_SQL = """
            SELECT product_id
            FROM public.shopping_carts
            WHERE user_id = :user_id
            """
        self.__DROP_USERS_PRODUCT_CART_SQL = """
            DELETE FROM public.shopping_carts
            WHERE user_id = :user_id;
            """

    def add_product_to_cart(self, user_id: int, product_id: int):
        self.__db.execute(self.__ADD_PRODUCT_TO_CART_SQL, {
            "user_id": user_id, "product_id": product_id})

    def drop_product_from_users_cart(self, user_id: int, product_id: int):
        self.__db.execute(self.__DROP_PRODUCT_FROM_USERS_CART_SQL, {
            "user_id": user_id, "product_id": product_id})

    def get_users_products(self, user_id: int) -> list[int]:
        result: list[int] = []
        query_result = self.__db.query(
            self.__GET_USERS_PRODUCTS_SQL, {"user_id": user_id})

        for row in query_result:
            result.append(row.product_id)

        return result

    def drop_users_product_cart(self, user_id: int):
        self.__db.query(self.__DROP_USERS_PRODUCT_CART_SQL,
                        {"user_id": user_id})
