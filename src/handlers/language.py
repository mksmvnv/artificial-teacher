import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.texts import messages

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("LANG_"))
async def handle_language_selection(callback: CallbackQuery) -> None:
    """Handle language selection."""
    callback_data = callback.data

    if not isinstance(callback_data, str):
        logger.warning("Callback data is not a string: %s", callback_data)
        return None

    lang_code = callback_data.split("_")[1]
    logger.info("User %d selected language %s", callback.from_user.id, lang_code)

    await callback.answer()

    if not callback.message or not hasattr(callback.message, "edit_text"):
        logger.warning("Message not accessible for editing: %s", callback)
        return None

    await callback.message.edit_text(
        text=getattr(messages, f"LANG_{lang_code.upper()}_START"), reply_markup=None
    )
