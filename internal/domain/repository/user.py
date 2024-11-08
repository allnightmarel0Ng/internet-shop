from internal.infrastructure.postgres.database import Database
from internal.domain.model.user import User


class UserRepository:
    def __init__(self, db: Database):
        self.__db = db
        self.__authorization_sql = """SELECT id, name, login 
                                    FROM public.users 
                                    WHERE login = :login AND password = :password;"""

    def __map_to_user(query_result) -> User:
        return User(name=query_result[0], login=query_result[1])

    def authorize_user(self, login: str, password: str) -> User:
        return self.__map_to_user(self.__db.query(self.__authorization_sql,
                                                  {"login": login,
                                                   "password": password}))
