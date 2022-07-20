from aiogram import types, Dispatcher
from bot_data import bot, dp, admin_id, admin_chat
from text import text
from markups import cb
import markups as nav
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P
from bot_data import qiwi_token
from data_base.data import Database
import random
from markups import short_url

db = Database("data.db")
p2p = QiwiP2P(auth_key=qiwi_token)


class add_scheme(StatesGroup):
    scheme_id = State()
    scheme_difficulty = State()
    scheme_price = State()
    scheme_description = State()
    scheme_link = State()
    check_data = State()


class send(StatesGroup):
    text = State()
    check = State()


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, text[0].format(message.from_user.first_name), reply_markup=nav.main_menu)
    db.add_client(message.from_user.id)


async def command_add_scheme(message: types.Message):
    await bot.send_message(admin_id, text[4], reply_markup=nav.go_back)
    await add_scheme.scheme_id.set()


async def command_start_message(message: types.Message):
    await bot.send_message(admin_id, text[6], reply_markup=nav.go_back)
    await send.text.set()


async def admin_menu(message: types.Message):
    if message.from_user.id == admin_id:
        await bot.send_message(admin_id, text[3], reply_markup=nav.go_back)


@dp.callback_query_handler(cb.filter(action=["easy", "midd", "hard", "menu", "rule"]))
async def callback_main_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "easy":
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text="🥉 Лёгкие способы 🥉", reply_markup=nav.easy_menu())
    if action == "midd":
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text="🥈 Средние способы 🥈", reply_markup=nav.midd_menu())
    if action == "hard":
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text="🥇 Сложные способы 🥇", reply_markup=nav.hard_menu())
    if action == "menu":
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text="🔰 Главное меню", reply_markup=nav.main_menu)
    if action == "rule":
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text[2].format(admin_chat), reply_markup=nav.go_back)
    await call.answer()


# @dp.callback_query_handler(text_contains="#")
async def callback_scheme_menu(call: types.CallbackQuery):
    comment = str(str(call.from_user.id) + "_" + str(random.randint(1000, 99999)))
    bill = p2p.bill(amount=db.get_price(call.data[1:][:1], call.data[1:][1:5]), lifetime=15, comment=comment)  # amount=1 (можно поставить 1, чтобы покупать все за 1 руб. "для теста")
    db.add_check(call.from_user.id, bill.bill_id)
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=db.get_description(call.data[1:][:1], call.data[1:][1:5]),
                                reply_markup=nav.buy_method(url=bill.pay_url, bill=bill.bill_id, id=call.data[1:][:1], difficulty=call.data[1:][1:5]))
    await call.answer()


# @dp.callback_query_handler(text_contains="check_")
async def check(callback: types.CallbackQuery):
    diff = str(callback.data[-4:])
    id_method = int(callback.data[-5:][:1])
    data = callback.data[:-5]
    bill = str(data[6:])
    info = db.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            db.delete_check(bill)
            await bot.send_message(callback.from_user.id, "⚠ Успешная оплата ⚠")
            await bot.send_message(callback.from_user.id, text[1].format(short_url(db.get_link(id_method, diff)), admin_chat), disable_web_page_preview=True, reply_markup=nav.go_back)
        else:
            await bot.send_message(callback.from_user.id, "😱 Вы ещё не оплатили 😱")
    else:
        await bot.send_message(callback.from_user.id, "Счет не найдет")
    await callback.answer()


# @dp.callback_query_handler(text_contains="menu"), state="*")
async def stop_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "🔰 Главное меню", reply_markup=nav.main_menu)
    await message.answer()


# @dp.message_handlers(state=add_scheme.scheme_id)
async def add_scheme_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["scheme_id"] = message.text
    await bot.send_message(admin_id, "Хорошо, теперь введите сложность\nПример:\n\nЛегкая - easy\nСредняя - midd\nСложная - hard", reply_markup=nav.go_back)
    await add_scheme.next()


# @dp.message_handlers(state=add_scheme.scheme_id)
async def add_scheme_difficulty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["scheme_difficulty"] = message.text
    if data["scheme_difficulty"].lower() == "easy" or data["scheme_difficulty"].lower() == "midd" or data["scheme_difficulty"].lower() == "hard":
        if not db.exist_scheme(data['scheme_id'], data['scheme_difficulty']):
            await bot.send_message(admin_id, "Хорошо, теперь введите стоимость схемы", reply_markup=nav.go_back)
            await add_scheme.next()
        else:
            await bot.send_message(admin_id, "😱 Id и Сложность схемы уже существуют 😱", reply_markup=nav.main_menu)
            await state.finish()
    else:
        await bot.send_message(admin_id, "Ошибка. Проверьте правильность написания сложности!")


# @dp.message_handlers(state=add_scheme.scheme_id)
async def add_scheme_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["scheme_price"] = message.text
    await bot.send_message(admin_id, "Хорошо, теперь введите описание схемы", reply_markup=nav.go_back)
    await add_scheme.next()


# @dp.message_handlers(state=add_scheme.scheme_id)
async def add_scheme_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["scheme_description"] = message.text
    await bot.send_message(admin_id, "Хорошо, теперь введите ссылку на схему(не сокращенную)", reply_markup=nav.go_back)
    await add_scheme.next()


# @dp.message_handlers(state=add_scheme.scheme_id)
async def add_scheme_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["scheme_link"] = message.text
    await bot.send_message(admin_id, "Хорошо, проверьте данные", reply_markup=nav.go_back)
    await bot.send_message(admin_id, text[5].format(data["scheme_id"], data["scheme_difficulty"], data["scheme_price"], data["scheme_description"], data["scheme_link"]),
                           disable_web_page_preview=True, reply_markup=nav.go_back)
    await add_scheme.next()


# @dp.message_handlers(state=add_scheme.scheme_id)
async def check_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["access"] = message.text
    if data["access"].lower() == "да":
        await bot.send_message(admin_id, "Хорошо, я добавил схему", reply_markup=nav.main_menu)
        db.add_scheme(data["scheme_id"], data["scheme_price"], data["scheme_difficulty"], data["scheme_description"], data["scheme_link"])
    await state.finish()


# @dp.message_handler(state=send.text)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await bot.send_message(admin_id, text[7].format(data["text"]), reply_markup=nav.go_back)
    await send.next()


# @dp.message_handler(state=send.check)
async def get_check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["check"] = message.text
    if data["check"].lower() == "да":
        await bot.send_message(admin_id, "Рассылка начинается")
        for i in db.get_users():
            try:
                await bot.send_message(i[0], data["text"])
            except: pass
        await bot.send_message(admin_id, "Рассылка завершена", nav.main_menu)
        await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(admin_menu, commands=["admin"])
    dp.register_message_handler(command_start_message, commands=["message"])
    dp.register_message_handler(command_add_scheme, commands=["addscheme"])
    dp.register_callback_query_handler(callback_scheme_menu, text_contains="#")
    dp.register_callback_query_handler(check, text_contains="check_")
    dp.register_callback_query_handler(stop_state, cb.filter(action=["menu"]), state="*")
    dp.register_message_handler(add_scheme_id, state=add_scheme.scheme_id)
    dp.register_message_handler(add_scheme_difficulty, state=add_scheme.scheme_difficulty)
    dp.register_message_handler(add_scheme_price, state=add_scheme.scheme_price)
    dp.register_message_handler(add_scheme_description, state=add_scheme.scheme_description)
    dp.register_message_handler(add_scheme_link, state=add_scheme.scheme_link)
    dp.register_message_handler(check_data, state=add_scheme.check_data)
    dp.register_message_handler(get_text, state=send.text)
    dp.register_message_handler(get_check, state=send.check)