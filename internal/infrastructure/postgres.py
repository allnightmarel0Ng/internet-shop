from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session


class NoResultFound(BaseException):
    """Raised when a query returns no result."""
    pass


class MultipleResultsFound(BaseException):
    """Raised when a query returns more than one result."""
    pass


class Database:
    def __init__(self, connection_string: str):
        self.__engine = create_engine(connection_string)
        self.__session_local = sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=self.__engine)
        self.__db: Session = self.__session_local()

    def query(self, sql: str, params: dict = None):
        query = text(sql)
        result = self.__db.execute(query, params)
        return result.fetchall()

    def query_row(self, sql: str, params: dict = None):
        query = text(sql)
        result = self.__db.execute(query, params)

        row = result.fetchone()
        if row is None:
            raise NoResultFound("No result found for the query.")

        rows = result.fetchall()
        if rows:
            raise MultipleResultsFound("Multiple results found for the query")

        return row

    def close(self):
        self.__db.close()

    def __del__(self):
        self.close()
