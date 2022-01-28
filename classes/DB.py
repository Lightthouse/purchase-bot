import sqlite3
from config.config import DB_FILE, CREATE_TABLE
from math import inf


class DB:

    __db_connect = None
    __cursor = None
    __table_name = None

    def __init__(self, table_name: str):
        self.__table_name = table_name

        tabl_exist = self.__execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='{table_name}' ", True)
        if not tabl_exist:
            self.__create_table()

    def __create_table(self):
        with open(CREATE_TABLE, "r") as f:
            sql = f.read()
        self.__cursor.executescript(sql)
        self.__db_connect.commit()

    def __execute(self, request: str, fetch_raws=0):

        self.__db_connect = sqlite3.connect(DB_FILE)
        self.__cursor = self.__db_connect.cursor()

        try:
            self.__cursor.execute(request)

            if fetch_raws == 1:
                return self.__cursor.fetchone()

            if fetch_raws > 1:
                return self.__cursor.fetchall()

            self.__db_connect.commit()
            return True
        except sqlite3.Error:
            return False

        finally:
            self.__cursor.close()

    def __where_statement(self,  eq_condition: dict, gt_condition: dict, lt_condition: dict):
        where = ''

        if eq_condition:
            where += ' and '.join([f'{i[0]}="{i[1]}"' for i in eq_condition.items()])

        if gt_condition:
            where += ' and '.join([f'{i[0]}>"{i[1]}"' for i in gt_condition.items()])

        if lt_condition:
            where += ' and '.join([f'{i[0]}<"{i[1]}"' for i in gt_condition.items()])

        return where if not where else 'WHERE ' + where

    def create(self, insert_data: dict):
        column_names = ','.join(insert_data.keys())
        column_values = ','.join([f'"{i}"' for i in insert_data.values()])
        return self.__execute(f'INSERT INTO {self.__table_name} ({column_names}) values ({column_values})')

    def select_all(self, eq: dict = None, gt: dict = None, lt: dict = None, columns='*'):
        where = self.__where_statement(eq, gt, lt)
        return self.__execute(f'SELECT {columns} FROM {self.__table_name} {where}', inf)

    def select(self, eq: dict = None, gt: dict = None, lt: dict = None, columns='*'):
        where = self.__where_statement(eq, gt, lt)
        return self.__execute(f'SELECT {columns} FROM {self.__table_name} {where}', 1)

    def delete(self, delete_key: str, delete_value: [str, int]):
        where = f'WHERE {delete_key}="{delete_value}"'
        return self.__execute(f'DELETE FROM {self.__table_name} {where}')
