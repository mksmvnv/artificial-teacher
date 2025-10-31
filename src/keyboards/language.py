from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Language:
    """Languages."""

    ENGLISH: str = "Английский 🇺🇸"

    @staticmethod
    def get_callback_data(lang_code: str) -> str:
        """Get callback data for language."""
        return f"LANG_{lang_code}"


class CEFRLevel:
    """CEFR levels."""

    A1: str = "A1 🪹"
    A2: str = "A2 🐣"
    B1: str = "B1 🐥"
    B2: str = "B2 🐦"
    C1: str = "C1 🦅"
    C2: str = "C2 🦉"

    @staticmethod
    def get_callback_data(level: str) -> str:
        """Get callback data for CEFR level."""
        return f"CEFR_{level}"


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


def get_cefr_keyboard() -> InlineKeyboardMarkup:
    """Get CEFR levels keyboard."""
    builder = InlineKeyboardBuilder()

    levels = [
        (CEFRLevel.A1, "A1"),
        (CEFRLevel.A2, "A2"),
        (CEFRLevel.B1, "B1"),
        (CEFRLevel.B2, "B2"),
        (CEFRLevel.C1, "C1"),
        (CEFRLevel.C2, "C2"),
    ]

    for text, level in levels:
        builder.add(
            InlineKeyboardButton(text=text, callback_data=CEFRLevel.get_callback_data(level))
        )

    builder.adjust(1)
    return builder.as_markup()
