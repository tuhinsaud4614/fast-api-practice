import sqlite3

from .utils import join_path


class Database:
    instance = None
    cur = None

    @staticmethod
    def connection():
        if Database.instance is None:
            Database.instance = sqlite3.connect(join_path("db.sqlite"))
            Database.cur = Database.instance.cursor()

    @staticmethod
    def close():
        if Database.instance:
            Database.instance.close()
    
