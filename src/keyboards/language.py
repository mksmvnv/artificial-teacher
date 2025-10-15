from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Language:
    """Languages."""

    ENGLISH: str = "English 🇺🇸"

    @staticmethod
    def get_callback_data(lang_code: str) -> str:
        """Get callback data for language."""
        return f"LANG_{lang_code}"


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get languages keyboard."""
    builder = InlineKeyboardBuilder()

    languages = [
        (Language.ENGLISH, "EN"),
    ]

    for text, lang_code in languages:
        builder.add(
            InlineKeyboardButton(text=text, callback_data=Language.get_callback_data(lang_code))
        )

    builder.adjust(1)
    return builder.as_markup()
