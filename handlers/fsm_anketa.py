from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from Keyboards import client_lb
from config import KURATORS


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.message):
    if message.from_user.id in KURATORS and message.text.startswith('/reg'):
        if message.chat.type == "private":
            await FSMAdmin.id.set()
            await message.answer("Укажите ID", reply_markup=client_lb.cancel_markup)
        else:
            await message.answer("Пишите в личку")
    elif not message.from_user.id in KURATORS and message.text.startswith('/reg'):
        await message.answer("Вы не являетесь администратором (КУРАТОРОМ)")


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
        data['name'] = message.text
        if not message.text in {data['name']} == '/reg':
            await FSMAdmin.next()
            await message.answer("Укажите имя", reply_markup=client_lb.cancel_markup)

        elif message.text in {data['name']} == '/reg':
            await message.answer("Вы не являетесь администратором (КУРАТОРОМ)")
            await state.finish()


async def load_name(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Укажите корректное имя без цифр")
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.answer("Укажите напрваление", reply_markup=client_lb.direction_markup)


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите возраст", reply_markup=client_lb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Укажите корректный возраст без букв")
    elif int(message.text) < 10 or int(message.text) > 100:
        await message.answer("Возрастное ограничение")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Укажите группу", reply_markup=client_lb.group_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(f"id ментора: {data['id']}\n"
                             f"Имя ментора: {data['name']}\n"
                             f"Направление: {data['direction']}\n"
                             f"Возраст ментора: {data['age']}\n"
                             f"Группа ментора: {data['group']}\n")
    await FSMAdmin.next()
    await message.answer("ЗАВЕРШИТЬ?", reply_markup=client_lb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ЗАВЕРШИТЬ":
        await state.finish()
        await message.answer("Регистрация завершена!")

    elif message.text == "ЗАНОВО":
        await FSMAdmin.id.set()
        await message.answer("Укажите ID")
    else:
        await message.answer("Подтвердите действие:(ЗАВЕРШИТЬ) (ЗАНОВО)")


async def cancel_register(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Регистрация отменена")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
    dp.register_message_handler(cancel_register, Text(equals='отмена', ignore_case=True), state='*')