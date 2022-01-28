from .DB import DB
from config.config import CATEGORY_TABLE
from slugify import slugify
from collections import namedtuple


CategoryRaw = namedtuple('CategoryRaw', 'name codename aliases')


class Category:
    __db = None
    __table_columns = ('codename', 'name', 'aliases')
    __default_name = 'прочее'

    def __init__(self):
        self.__db = DB(CATEGORY_TABLE)

    def add(self, name: str, codename=None, aliases=''):
        codename = codename if codename else slugify(name)
        return self.__db.create({'codename': codename, 'name': name, 'aliases': aliases})

    def list(self):
        return self.__db.select_all()

    def get_codename(self, name=None):
        name = name if name else self.__default_name
        category = self.__db.select(eq={'name': name}, columns='codename')

        if not category:
            category = self.__db.select(eq={'name': self.__default_name}, columns='codename')

        return category[0]

    def category_exist(self, name: str):
        category = self.__db.select(eq={'name': name}, columns='codename')
        return bool(category)

    def remove(self, codename: str):
        return self.__db.delete('codename', codename)
