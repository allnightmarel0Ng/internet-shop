from internal.infrastructure.postgres.database import Database
from internal.domain.model.shop import Shop


class ShopRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__authorization_sql = """SELECT id, name, login 
                                    FROM public.shops 
                                    WHERE login = :login AND password = :password;"""

    def __map_to_shop(query_result) -> Shop:
        return Shop(name=query_result[0], login=query_result[1])

    def authorize_shop(self, login: str, password: str) -> Shop:
        return self.__map_to_shop(self.__db.query(self.__authorization_sql,
                                                  {"login": login,
                                                   "password": password}))
