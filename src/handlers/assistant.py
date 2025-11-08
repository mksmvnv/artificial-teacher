import logging

from aiogram import F, Router
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from src.services import AssistantService, ContextService, LanguageService
from src.texts import messages

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text)
@inject
async def handle_chat_message(
    message: Message,
    assistant_service: FromDishka[AssistantService],
    context_service: FromDishka[ContextService],
    language_service: FromDishka[LanguageService],
) -> None:
    """Handle user messages for AI assistant."""
    if not message.from_user:
        logger.warning("User not found in message '%s'", message)
        return None

    user_tg_id = message.from_user.id
    user_message = message.text

    if not user_message:
        logger.warning("User '%s' message is empty", user_tg_id)
        return None

    # Get user language from context or database
    language = await context_service.get_context(prefix="user_language", user_tg_id=user_tg_id)
    if not language:
        language = await language_service.get_user_language(user_tg_id=user_tg_id)
        if not language:
            await message.answer(messages.SELECT_LANGUAGE_SKILLS.format(skill="язык"))
            return None

    # Get CEFR level from context or database
    cefr_level = await context_service.get_context(prefix="user_cefr_level", user_tg_id=user_tg_id)
    if not cefr_level:
        cefr_level = await language_service.get_user_cefr_level(user_tg_id=user_tg_id)
        if not cefr_level:
            await message.answer(
                messages.SELECT_LANGUAGE_SKILLS.format(skill="уровень владения языком")
            )
            return None

    if not message.bot:
        logger.warning("Bot not found in message '%s'", message)
        return None

    # Show typing action
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Get response from assistant
    response = await assistant_service.chat(
        user_tg_id=user_tg_id, message=user_message, language=language, cefr_level=cefr_level
    )

    if response:
        await message.answer(response)
    else:
        await message.answer(getattr(messages, f"{language.upper()}_ERROR_MESSAGE"))
