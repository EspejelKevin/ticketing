from mysql.connector import connect

from typing import Self


class MySQL:
    def __init__(self, host: str, user: str, password: str, db: str) -> None:
        self._connection = connect(user=user, password=password, host=host, database=db)

    def __enter__(self) -> Self:
        return self

    def get_session(self):
        return self._connection

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self._connection.commit()
        else:
            self._connection.rollback()
