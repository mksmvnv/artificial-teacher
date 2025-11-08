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


@router.callback_query(F.data.startswith("lang_"))
@inject
async def handle_language_selection(
    callback: CallbackQuery,
    language_service: FromDishka[LanguageService],
    context_service: FromDishka[ContextService],
) -> None:
    """Handle language selection."""
    callback_data = callback.data
    user_tg_id = callback.from_user.id

    if not isinstance(callback_data, str):
        logger.warning("Callback data '%s' is not a string", callback_data)
        return None

    language = callback_data.split("_")[1]

    # Set language in context and database
    await gather(
        language_service.set_user_language(user_tg_id=user_tg_id, language=language),
        context_service.set_context(prefix="user_language", user_tg_id=user_tg_id, data=language),
    )

    await callback.answer()

    if not callback.message or not hasattr(callback.message, "edit_text"):
        logger.warning("Message '%s' not accessible for editing", callback)
        return None

    await callback.message.edit_text(
        text=getattr(messages, f"{language.upper()}_LANGUAGE_START"),
        reply_markup=get_cefr_keyboard(),
    )


@router.callback_query(F.data.startswith("cefr_level_"))
@inject
async def handle_cefr_level_selection(
    callback: CallbackQuery,
    language_service: FromDishka[LanguageService],
    context_service: FromDishka[ContextService],
) -> None:
    """Handle CEFR level selection."""
    callback_data = callback.data
    user_tg_id = callback.from_user.id

    if not isinstance(callback_data, str):
        logger.warning("Callback data '%s' is not a string", callback_data)
        return None

    # Get language from context or database
    language = await context_service.get_context(prefix="user_language", user_tg_id=user_tg_id)

    if not language:
        language = await language_service.get_user_language(user_tg_id=user_tg_id)
        if not language:
            return None

    cerf_level = callback_data.split("_")[2]

    # Set CEFR level in context and database
    await gather(
        language_service.set_user_cefr_level(user_tg_id=user_tg_id, cefr_level=cerf_level),
        context_service.set_context(
            prefix="user_cefr_level", user_tg_id=user_tg_id, data=cerf_level
        ),
    )

    await callback.answer()

    if not callback.message or not hasattr(callback.message, "edit_text"):
        logger.warning("Message '%s' not accessible for editing", callback)
        return None

    await callback.message.edit_text(
        text=getattr(messages, f"{language.upper()}_CEFR_START"), reply_markup=None
    )
