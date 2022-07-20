from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import pyshorteners
from data_base.data import Database
from bot_data import group_link

cb = CallbackData("fabnum", "action")
db = Database('data.db')


def short_url(url):
    try:
        return pyshorteners.Shortener().clckru.short(url)
    except:
        print("Url error")
        return url

main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(InlineKeyboardButton("🥉 Легкие способы 🥉", callback_data=cb.new(action="easy")),
              InlineKeyboardButton("🥈 Средние способы 🥈", callback_data=cb.new(action="midd")),
              InlineKeyboardButton("🥇 Сложные способы 🥇", callback_data=cb.new(action="hard"))).row(
              InlineKeyboardButton("🗒 Описание", callback_data=cb.new(action="rule")),
              InlineKeyboardButton("✅ Отзывы", url=group_link))


go_back = InlineKeyboardMarkup()
go_back.add(InlineKeyboardButton("🔰 Главное меню", callback_data=cb.new(action="menu")))


def buy_method(url="", bill="", id=1, difficulty=""):
    pay_menu = InlineKeyboardMarkup(row_width=2)
    pay_url = InlineKeyboardButton(text="Оплатить", url=short_url(url))
    pay_check = InlineKeyboardButton(text="Проверить", callback_data="check_"+bill+str(id)+difficulty)
    go_menu = InlineKeyboardButton(text="💾 Меню 💾", callback_data=cb.new(action="menu"))
    pay_menu.add(pay_url, pay_check, go_menu)
    return pay_menu


def easy_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(1, db.get_scheme_amount('easy') + 1):
        menu.add(InlineKeyboardButton(f"#{i} Схема {db.get_price(i, 'easy')} руб.", callback_data=f"#{i}easy"))
    menu.add(InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action="menu")))
    return menu


def midd_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(1, db.get_scheme_amount('midd') + 1):
        menu.add(InlineKeyboardButton(f"#{i} Схема {db.get_price(i, 'midd')} руб.", callback_data=f"#{i}midd"))
    menu.add(InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action="menu")))
    return menu


def hard_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(1, db.get_scheme_amount('hard') + 1):
        menu.add(InlineKeyboardButton(f"#{i} Схема {db.get_price(i, 'hard')} руб.", callback_data=f"#{i}hard"))
    menu.add(InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action="menu")))
    return menu
