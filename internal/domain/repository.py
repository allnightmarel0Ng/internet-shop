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

    def __map_to_user(query_result) -> User:
        return User(name=query_result[0], login=query_result[1], balance=query_result[2])

    def authorize_user(self, login: str, password: str) -> User:
        return self.__map_to_user(self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login, "password": password}
        ))


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

    def __map_to_product(query_result) -> Product:
        return Product(Category(query_result[0]), Shop(query_result[1], query_result[2]), query_result[3], float(query_result[4]), query_result[5])

    def get_product_by_id(self, id: int):
        return self.__map_to_product(self.__db.query_row(
            self.__GET_BY_ID_SQL, {"id": id}
        ))
