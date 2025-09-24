import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import settings
from src.utils.logger import logger


async def main() -> None:
    """Main application entry point."""
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    logger.info("LinguAI Pro bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
