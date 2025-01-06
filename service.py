from database import pool, execute_update_query, execute_select_query, quiz_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    if current_question_index < len(quiz_data):
        question_data = quiz_data[current_question_index]
        correct_index = question_data['correct_option']
        opts = question_data['options']
        kb = generate_options_keyboard(opts, opts[correct_index])
        await message.answer(f"{question_data['question']}", reply_markup=kb)
    else:
        await message.answer("Это был последний вопрос. Квиз завершен!")

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index,total_points = 0)
    await get_question(message, user_id)


async def get_quiz_index(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT question_index
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["question_index"] is None:
        return 0
    return results[0]["question_index"]    

async def get_total_points(user_id):
    get_user_points = f"""
        DECLARE $user_id AS Uint64;

        SELECT total_points
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_points, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["total_points"] is None:
        return 0
    return results[0]["total_points"]       
    

async def update_quiz_index(user_id, question_index,total_points):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;
        DECLARE $total_points AS Uint64;

        UPSERT INTO `quiz_state` (`user_id`, `question_index`, `total_points`)
        VALUES ($user_id, $question_index, $total_points);
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=question_index,
        total_points=total_points,
    )
