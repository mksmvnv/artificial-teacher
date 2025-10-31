import logging
from asyncio import gather

from aiogram import F, Router
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import FromDishka, inject

from src.keyboards.language import get_cefr_keyboard
from src.services import ContextService, LanguageService
from src.texts import messages

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("LANG_"))
@inject
async def handle_language_selection(
    callback: CallbackQuery,
    language_service: FromDishka[LanguageService],
    context_service: FromDishka[ContextService],
) -> None:
    """Handle language selection."""
    callback_data = callback.data
    tg_id = callback.from_user.id

    if not isinstance(callback_data, str):
        logger.warning("Callback data is not a string: %s", callback_data)
        return None

    if not callback.message or not hasattr(callback.message, "edit_text"):
        logger.warning("Message not accessible for editing: %s", callback)
        return None

    language = callback_data.split("_")[1]

    # Set language in context and database
    await gather(
        language_service.set_user_language(tg_id=tg_id, language=language),
        context_service.set_user_language(tg_id=tg_id, language=language),
    )

    await callback.answer()

    await callback.message.edit_text(
        text=getattr(messages, f"LANG_{language.upper()}_START"), reply_markup=get_cefr_keyboard()
    )


@router.callback_query(F.data.startswith("CEFR_"))
@inject
async def handle_cefr_level_selection(
    callback: CallbackQuery,
    language_service: FromDishka[LanguageService],
    context_service: FromDishka[ContextService],
) -> None:
    """Handle CEFR level selection."""
    callback_data = callback.data
    tg_id = callback.from_user.id

    if not isinstance(callback_data, str):
        logger.warning("Callback data is not a string: %s", callback_data)
        return None

    # Get language from context or database
    language = await context_service.get_user_language(tg_id=tg_id)

    if not language:
        logger.warning("State does not contain language for user %d", tg_id)
        language = await language_service.get_user_language(tg_id=tg_id)
        if not language:
            logger.warning("User %d language not found in database", tg_id)
            return None

    await callback.answer()

    if not callback.message or not hasattr(callback.message, "edit_text"):
        logger.warning("Message not accessible for editing: %s", callback)
        return None

    cerf_level = callback_data.split("_")[1]

    await language_service.set_user_cefr_level(tg_id=callback.from_user.id, cefr_level=cerf_level)

    await callback.message.edit_text(
        text=getattr(messages, f"CEFR_{language.upper()}_START"), reply_markup=None
    )
