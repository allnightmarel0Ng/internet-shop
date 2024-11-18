from internal.infrastructure.postgres import Database
from internal.domain.model import *


class UserRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__AUTHORIZATION_SQL = """
            SELECT name, login, balance 
            FROM public.users 
            WHERE login = :login AND password = :password;
            """
        self.__CHANGE_BALANCE_SQL = """
            UPDATE public.users
            SET balance = balance + (:diff)
            WHERE login = :login;
            """
        self.__GET_ID_BY_LOGIN = """
            SELECT id
            FROM public.users
            WHERE login = :login
            """

    def __map_to_user(query_result) -> User:
        return User(name=query_result[0], login=query_result[1], balance=query_result[2])

    def authorize_user(self, login: str, password: str) -> User:
        return self.__map_to_user(self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login, "password": password}
        ))

    def change_balance(self, login: str, diff: int):
        self.__db.query(
            self.__CHANGE_BALANCE_SQL,
            {"login": login, "diff": diff})
        
    def get_id_by_login(self, login: str) -> int:
        return self.__db.query_row(self.__GET_ID_BY_LOGIN, {"login": login})


class ShopRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__AUTHORIZATION_SQL = """
            SELECT name, login 
            FROM public.shops 
            WHERE login = :login AND password = :password;
            """

    def __map_to_shop(query_result) -> Shop:
        return Shop(name=query_result[0], login=query_result[1])

    def authorize_shop(self, login: str, password: str) -> Shop:
        return self.__map_to_shop(self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login, "password": password}
        ))


class CategoryRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__GET_BY_ID_SQL = """
            SELECT name 
            FROM public.categories 
            WHERE id = :id;
            """

    def __map_to_category(query_result) -> Category:
        return Category(query_result[0])

    def get_category_by_id(self, id: int) -> Category:
        return self.__map_to_category(self.__db.query_row(
            self.__GET_BY_ID_SQL, {"id", id}
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

    def __map_to_product(query_result) -> Product:
        return Product(Category(query_result[0]), Shop(query_result[1], query_result[2]), query_result[3], float(query_result[4]), query_result[5])

    def get_product_by_id(self, id: int) -> Product:
        return self.__map_to_product(self.__db.query_row(
            self.__GET_BY_ID_SQL, {"id": id}
        ))
    
    def get_products_price_sum(self, ids: list[int]) -> int:
        values = ' (' + ', '.join(str(id) for id in ids) + ');'
        result = 0
        query_result = self.__db.query(self.__GET_SUM_PRICE_BY_IDS_SQL + values)
        
        for row in query_result:
            result += row.price

        return result


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

    def get_user_paychecks(self, user_id: int) -> list[Paycheck]:
        # feels buggy...
        result: list[Paycheck] = []
        query_result = self.__db.query(
            self.__GET_PAYCHECKS_BY_USER_ID, {"id": user_id})

        current = Paycheck(id=-1)
        price = 0

        for row in query_result:
            if row.paycheck_id != current.id and current.id != -1:
                result.append(current)
                price = 0

            product_price = float(product_price)
            price += product_price

            current.id = row.paycheck_id
            current.user = User(
                row.user_name, row.user_login, row.user_balance)
            current.products.append(Product(Category(row.category_name), Shop(
                row.shop_name, row.shop_login), row.product_name, row.product_price, row.product_description))

        return result

    def add_paycheck_for_user(self, user_id: int, product_ids: list[int]):
        values = ', '.join(self.__ADD_PAYCHECK_VALUE_TEMPLATE_SQL.format(
            user_id=user_id, product_id=product_id) for product_id in product_ids)
        self.__db.query(self.__ADD_PAYCHECK_SQL + values)


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
            FROM public.shoppint_carts
            WHERE user_id = :user_id
            """
        self.__DROP_USERS_PRODUCT_CART_SQL = """
            DELETE FROM public.shopping_carts
            WHERE user_id = :user_id;
            """
        
    def add_product_to_card(self, user_id: int, product_id: int):
        self.__db.query(self.__ADD_PRODUCT_TO_CART_SQL, {"user_id": user_id, "product_id": product_id})
    
    def drop_product_from_users_cart(self, user_id: int, product_id: int):
        self.__db.query(self.__DROP_PRODUCT_FROM_USERS_CART_SQL, {"user_id": user_id, "product_id": product_id})
    
    def get_users_products(self, user_id: int) -> list[int]:
        result: list[int] = []
        query_result = self.__db.query(self.__GET_USERS_PRODUCTS_SQL, {"user_id": user_id})
        
        for row in query_result:
            result.append(row.product_id)
        
        return result
    
    def drop_users_product_cart(self, user_id: int):
        self.__db.query(self.__DROP_USERS_PRODUCT_CART_SQL, {"user_id": user_id})