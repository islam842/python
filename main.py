from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ParseMode
import logging

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)



@dp.message_handler(commands=['quiz'])
async def quiz(message: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("NEXT", callback_data="button")
    markup.add(button)

    question = "В каком году были основаны курсы Geeks?"
    answers = [
        "2019",
        "2018",
        "2017",
        "2020",
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Раньше были курсы GeekTech потом был ренбрендинг и переименовали на Geeks",
        open_period=15,
        reply_markup=markup


    )

@dp.callback_query_handler(text="button")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("NEXT", callback_data="button1")
    markup.add(button)

    question = "Сколько направлений есть на курсах Geeks?"
    answers = [
        "6",
        "8",
        "5",
        "7",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="IOS, Android, PM, Backend, Frontend, UX/UI, Основы программирование, Fullstack",
        open_period=15,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button1")
async def quiz_3(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("NEXT", callback_data="button2")
    markup.add(button1)

    question = "Кто основатели курсов Geeks?"
    answers = [
        "Талантбеков Ислам и Нургазы Сулайманов",
        "Айдар Бакиров и Сулаймaнов Бакир",
        "Нургазы Сулайманов и Айдар Бакиров",
        "Сулаймнов Айдар и Бекболот Бакиров",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Стыдно не знать(",
        open_period=20,
        reply_markup=markup
    )

@dp.callback_query_handler(text="button2")
async def quiz_3(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("NEXT", callback_data="button3")
    markup.add(button2)

    question = "Сколько длится fullstack направление?"
    answers = [
        "8м",
        "11м",
        "10м",
        "9м",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Стыдно не знать(",
        open_period=20,
        reply_markup=markup
    )

@dp.message_handler(commands=['mem'])
async def mem(message: types.message):
     with open('images/993ea740-1170-45d6-8e95-c8618a2cc586.tmp', 'rb') as img:
         await message.answer_photo(photo=img)

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.strip().isdigit():
        num = int(message.text.strip())
        square = num ** 2
        await message.reply(square)
    else:
        await message.reply(message.text)

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
