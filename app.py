import telebot
import os
from config.config import TELEGRAM_TOKEN
from classes import Category, Purchase, StringFormat
from exceptions import PurchaseException, DBException
import pprint
import re
import emoji

category = Category()
purchase = Purchase()

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я сказала стартуем')


@bot.message_handler(commands=["help"])
def help(m):
    bot.send_message(m.chat.id,
                     'Для добавления покупки в список, введите команду в формате: [цена] [название] [категория]')


@bot.message_handler(commands=["cow_say"])
def stepan(m):
    bot.send_message(m.chat.id, 'mooo')


@bot.message_handler(commands=["categories"])
def categories(m):
    pretty_categories = StringFormat.categories_list(category.list())
    bot.send_message(m.chat.id, "Категории покупок")
    bot.send_message(m.chat.id, pretty_categories)


@bot.message_handler(func=lambda message: message.text.startswith('/sum'))
def summary(message):
    text = message.text.replace('/sum', '').replace(' ', '')

    digit = re.search(r'\d+', text) or 0
    days_offset = int(digit.group()) * 24 if digit else None

    chars = re.sub(r'\d', '', text)
    category_name = category.get_codename(chars) if category.category_exist(chars) else None

    purchase_sum = purchase.sum(category=category_name, hours_offset=days_offset)
    bot.send_message(message.chat.id, emoji.emojize(f'Сумма покупок: :heavy_dollar_sign: {purchase_sum}'))


@bot.message_handler(func=lambda message: message.text.startswith('/list'))
def list_purchases(message):
    text = message.text.replace('/list', '').replace(' ', '')

    digit = re.search(r'\d+', text) or 0
    days_offset = int(digit.group()) * 24 if digit else None

    chars = re.sub(r'\d', '', text)
    category_name = category.get_codename(chars) if category.category_exist(chars) else None

    lst = purchase.list(category=category_name, hours_offset=days_offset)
    pretty_purchases = StringFormat.purchases_list(lst)

    bot.send_message(message.chat.id, 'Список покупок')
    bot.send_message(message.chat.id, pretty_purchases)


@bot.message_handler(func=lambda message: message.text.startswith('/del'))
def summary(message):
    text = message.text.replace('/del', '').replace(' ', '')

    digit = re.search(r'\d+', text) or 0
    purchase_id = int(digit.group()) * 24 if digit else None

    purchase_removed = purchase.remove(purchase_id)
    result_message = emoji.emojize('Покупка добавлена :check_mark_button:')

    if not purchase_removed:
        result_message = emoji.emojize('Передан некорректный id товара :cross_mark:')

    bot.send_message(message.chat.id, result_message)


@bot.message_handler(content_types='text')
def text_handler(message):
    bot.send_message(message.chat.id, 'tyta')
    try:
        add_raw = purchase.extract_purchase_command(message.text)
        purchase.add(add_raw)

        bot.send_message(message.chat.id, emoji.emojize('Покупка добавлена 	:check_mark_button:'))
    except PurchaseException as prexcp:
        bot.send_message(message.chat.id, 'Некорректный ввод строки')
    except DBException as dbexcp:
        bot.send_message(message.chat.id, 'Ошибка хранилища данных')




bot.polling(none_stop=True, interval=0)
