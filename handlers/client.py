from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from aiogram import Dispatcher, types


async def quiz_command(message: types.CallbackQuery):
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
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Раньше были курсы GeekTech потом был ренбрендинг и переименовали на Geeks",
        open_period=15,
        reply_markup=markup

    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(quiz_command, commands=['quiz'])



