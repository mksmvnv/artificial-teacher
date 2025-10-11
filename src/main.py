import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.core.config import settings
from src.core.providers import DatabaseProvider, RepositoryProvider, ServiceProvider
from src.handlers import start


async def main() -> None:
    """Configure and start bot."""
    logging.basicConfig(
        level=settings.logger.level,
        format=settings.logger.format,
        handlers=[
            logging.FileHandler(settings.logger.path),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)

    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(start.router)

    container = make_async_container(
        DatabaseProvider(), RepositoryProvider(), ServiceProvider(), AiogramProvider()
    )
    setup_dishka(container=container, router=dp, auto_inject=True)

    logger.info("LinguAI Pro started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
