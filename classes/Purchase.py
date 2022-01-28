from .DB import DB
from .Category import Category
from exceptions import PurchaseException
from config.config import PURCHASE_TABLE
from slugify import slugify
from collections import namedtuple
import pendulum


PurchaseRaw = namedtuple('PurchaseRaw', 'amount name category')


class Purchase:
    __db = None
    __category = None
    __table_columns = ('category_codename', 'amount', 'name', 'created', 'id')
    __date_format = 'YYYY-MM-DD HH:mm:ss'  # '2022-01-27 14:33:28'

    def __init__(self):
        self.__db = DB(PURCHASE_TABLE)
        self.__category = Category()

    def __offset_string(self, hours):
        now = pendulum.now().add(hours=-hours)
        return now.format(self.__date_format)

    def extract_purchase_command(self, raw: str):
        words = raw.split()
        words_count = len(words)

        try:
            amount = words[0] if isinstance(words[0], int) else int(words[0])
            name = words[1] if words_count > 1 else ''
            category = words[2] if words_count > 2 else ''
        except Exception:
            raise PurchaseException('Некорректная строка добавления покупки.')

        return PurchaseRaw(amount, name, category)

    def add(self, input_raw: PurchaseRaw):
        category_codename = self.__category.get_codename(input_raw.category)
        return self.__db.create(
            {'category_codename': category_codename, 'name': input_raw.name, 'amount': input_raw.amount})

    def list(self, category='', hours_offset=0, one_raw=False):
        if any([category, hours_offset]):
            eq_statement = {'category_codename': category} if category else None
            gt_statement = {'created': self.__offset_string(hours_offset)} if hours_offset else {}

            if one_raw:
                return self.__db.select(eq=eq_statement, gt=gt_statement)
            return self.__db.select_all(eq=eq_statement, gt=gt_statement)

        return self.__db.select_all()

    def sum(self, category='', hours_offset=0, one_raw=False):
        raws = self.list(category=category, hours_offset=hours_offset, one_raw=one_raw)
        return 0 if not len(raws) else sum([r[1] for r in raws])

    def remove(self, purchase_id: int):
        return self.__db.delete(delete_key='id', delete_value=purchase_id)

