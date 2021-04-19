import sqlite3
from uuid import uuid4

from .database import Database


class USER:
    def __init__(self):
        if Database.instance and Database.cur:
            try:
                Database.cur.execute(f'''
                    CREATE TABLE users (
                        id TEXT NOT NULL UNIQUE PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        avatar TEXT NOT NULL,
                    )
                ''')
                Database.instance.commit()
            except sqlite3.Error as er:
                raise er
        else:
            raise Exception("Database Not Connected")

    def create(self, first_name: str, last_name: str, email: str, password: str, avatar: str):
        if Database.instance and Database.cur:
            try:
                Database.cur.execute(f'''
                    INSERT INTO users VALUES(
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                    )
                ''', (uuid4(), first_name, last_name, email, password, avatar))
                Database.instance.commit()
            except sqlite3.Error as er:
                raise er
        else:
            raise Exception("Database Not Connected")
