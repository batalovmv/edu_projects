from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from bot import bot, dp
from quiz_data import quiz_data
from database import get_user_state, update_user_state, reset_user_state, save_user_result, get_user_result
from aiogram.filters import Command

def register_handlers():
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.message.register(cmd_quiz, Command('quiz'))
    dp.message.register(cmd_stats, Command('stats'))
    dp.callback_query.register(handle_answer, F.data.startswith('answer_'))

async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    result = await get_user_result(user_id)
    if result is not None:
        await message.answer(f"Ваш последний результат: {result} правильных ответов из {len(quiz_data)}.")
    else:
        await message.answer("Вы еще не проходили квиз.")

async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def cmd_quiz(message: types.Message):
    await reset_user_state(message.from_user.id)
    await message.answer("Давайте начнем квиз!")
    await send_question(message.chat.id, message.from_user.id)

async def send_question(chat_id, user_id):
    question_index, _ = await get_user_state(user_id)
    if question_index < len(quiz_data):
        question_data = quiz_data[question_index]
        builder = InlineKeyboardBuilder()
        for idx, option in enumerate(question_data['options']):
            builder.add(types.InlineKeyboardButton(
                text=option,
                callback_data=f'answer_{idx}'
            ))
        builder.adjust(1)
        await bot.send_message(chat_id, question_data['question'], reply_markup=builder.as_markup())
    else:
        await show_result(chat_id, user_id)

async def handle_answer(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    question_index, correct_answers = await get_user_state(user_id)
    chosen_option = int(callback.data.split('_')[1])
    correct_option = quiz_data[question_index]['correct_option']

    await callback.message.delete_reply_markup()

    if chosen_option == correct_option:
        correct_answers += 1
        await callback.message.answer(f"✅ Верно! Ваш ответ: {quiz_data[question_index]['options'][chosen_option]}")
    else:
        correct_text = quiz_data[question_index]['options'][correct_option]
        await callback.message.answer(
            f"❌ Неправильно. Ваш ответ: {quiz_data[question_index]['options'][chosen_option]}\n"
            f"Правильный ответ: {correct_text}"
        )

    question_index += 1
    await update_user_state(user_id, question_index, correct_answers)

    if question_index < len(quiz_data):
        await send_question(callback.message.chat.id, user_id)
    else:
        await show_result(callback.message.chat.id, user_id)

async def show_result(chat_id, user_id):
    _, correct_answers = await get_user_state(user_id)
    total_questions = len(quiz_data)
    await bot.send_message(chat_id, f"Квиз завершен! Вы ответили правильно на {correct_answers} из {total_questions} вопросов.")

    await save_user_result(user_id, correct_answers)
    await reset_user_state(user_id)