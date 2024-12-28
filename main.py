import asyncio
import logging
from bot import bot, dp
from handlers import register_handlers
from database import create_table

logging.basicConfig(level=logging.INFO)

async def main():
    await create_table()
    register_handlers()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())