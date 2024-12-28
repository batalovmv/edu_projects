import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER,
                correct_answers INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                correct_answers INTEGER
            )
        ''')
        await db.commit()

async def save_user_result(user_id, correct_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_results (user_id, correct_answers)
            VALUES (?, ?)
        ''', (user_id, correct_answers))
        await db.commit()

async def get_user_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM quiz_results WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

async def get_user_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index, correct_answers FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result
            else:
                return (0, 0)

async def update_user_state(user_id, question_index, correct_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers)
            VALUES (?, ?, ?)
        ''', (user_id, question_index, correct_answers))
        await db.commit()

async def reset_user_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            UPDATE quiz_state
            SET question_index = ?, correct_answers = ?
            WHERE user_id = ?
        ''', (0, 0, user_id))
        await db.commit()