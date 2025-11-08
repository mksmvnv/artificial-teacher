import json
import logging

from huggingface_hub import AsyncInferenceClient

from src.core.config import settings
from src.services.context import ContextService
from src.texts.prompts import CHAT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class AssistantService:
    """AI assistant service."""

    def __init__(self) -> None:
        self._client = AsyncInferenceClient(token=settings.assistant.token.get_secret_value())
        self._context_service = ContextService()
        self._max_history_length = settings.context.max_history_length
        self._chat_system_prompt = CHAT_SYSTEM_PROMPT

    async def chat(
        self, user_tg_id: int, message: str, language: str, cefr_level: str
    ) -> str | None:
        """Chat with AI assistant."""
        chat_history = await self._get_chat_history(user_tg_id)

        # Add user message to history
        chat_history.append({"role": "user", "content": message})

        # Build messages
        messages = self._build_messages(language, cefr_level, chat_history)

        # Get assistant response
        response = await self._client.chat.completions.create(
            model=settings.assistant.model,
            messages=messages,
            max_tokens=settings.assistant.max_tokens,
            temperature=settings.assistant.temperature,
        )

        if not response.choices or not response.choices[0].message:
            logger.warning("Empty choices or message from assistant")
            return None

        response_text: str | None = response.choices[0].message.content

        if not response_text:
            logger.warning("Empty response from assistant")
            return None

        # Add assistant response to history
        chat_history.append({"role": "assistant", "content": response_text})

        # Trim history if exceeds limit and save
        if len(chat_history) > self._max_history_length:
            chat_history = chat_history[-self._max_history_length :]

        await self._set_chat_history(user_tg_id, chat_history)
        logger.info("Chat history updated for user %s", user_tg_id)

        return response_text

    async def _get_chat_history(self, user_tg_id: int) -> list[dict[str, str]]:
        """Get chat history from context."""
        context_data = await self._context_service.get_context(prefix="chat", user_tg_id=user_tg_id)

        if context_data:
            parsed_data: list[dict[str, str]] = json.loads(context_data)
            return parsed_data

        return []

    async def _set_chat_history(self, user_tg_id: int, history: list[dict[str, str]]) -> None:
        """Set chat history in context."""
        await self._context_service.set_context(
            prefix="chat", user_tg_id=user_tg_id, data=json.dumps(history)
        )

    def _build_messages(
        self, language: str, cefr_level: str, history: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Build messages for AI including system prompt and history."""
        # Format system prompt with language and CEFR level
        system_prompt = self._chat_system_prompt.format(
            language=language.title(), cefr_level=cefr_level.title()
        )

        # Add system prompt to messages
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)

        return messages
