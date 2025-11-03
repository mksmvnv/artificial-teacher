import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from src.keyboards.language import get_language_keyboard
from src.schemas.user import UserSchema
from src.services import StartService
from src.texts import messages

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
@inject
async def handle_start(message: Message, start_service: FromDishka[StartService]) -> None:
    """Handle /start command."""
    if not message.from_user:
        logger.warning("User not found in message '%s'", message)
        return None

    # Create user object
    user = UserSchema(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    await start_service.register_user(user)
    logger.info("User '%d' started bot", user.tg_id)
    await message.answer(text=messages.WELCOME, reply_markup=get_language_keyboard())
