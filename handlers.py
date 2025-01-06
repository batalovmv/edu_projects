from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from service import get_question, new_quiz, get_quiz_index, update_quiz_index,get_total_points
from database import quiz_data

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    total_points = await get_total_points(callback.from_user.id)
    total_points += 1
    await update_quiz_index(callback.from_user.id, current_question_index,total_points)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer( f"Это был последний вопрос. Квиз завершен! Ваш результат: {total_points} очков.")

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    correct_answer = quiz_data[current_question_index]['options'][correct_option]
    await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")
    current_question_index += 1
    total_points = await get_total_points(callback.from_user.id)
    await update_quiz_index(callback.from_user.id, current_question_index,total_points)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer( f"Это был последний вопрос. Квиз завершен! Ваш результат: {total_points} очков.")

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Начать игру")
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(F.text == "Начать игру")
async def cmd_quiz(message: types.Message):
    # URL публичного изображения
    image_url = "https://storage.yandexcloud.net/batalovmv-quiz-images/_.png"

    # Отправляем картинку с подписью
    await message.answer_photo(photo=image_url, caption="Добро пожаловать в квиз по Python! 🐍")
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)
