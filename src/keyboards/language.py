from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Language:
    """Languages."""

    ENGLISH: str = "Английский 🇺🇸"

    @staticmethod
    def get_callback_data(language: str) -> str:
        """Get callback data for language."""
        return f"lang_{language}"


class CEFRLevel:
    """CEFR levels."""

    A1: str = "A1 🪹"
    A2: str = "A2 🐣"
    B1: str = "B1 🐥"
    B2: str = "B2 🐦"
    C1: str = "C1 🦅"
    C2: str = "C2 🦉"

    @staticmethod
    def get_callback_data(cefr_level: str) -> str:
        """Get callback data for CEFR level."""
        return f"cefr_level_{cefr_level}"


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get languages keyboard."""
    builder = InlineKeyboardBuilder()

    languages = [
        (Language.ENGLISH, "english"),
    ]

    for text, language in languages:
        builder.add(
            InlineKeyboardButton(text=text, callback_data=Language.get_callback_data(language))
        )

    builder.adjust(1)
    return builder.as_markup()


def get_cefr_keyboard() -> InlineKeyboardMarkup:
    """Get CEFR levels keyboard."""
    builder = InlineKeyboardBuilder()

    cefr_levels = [
        (CEFRLevel.A1, "a1"),
        (CEFRLevel.A2, "a2"),
        (CEFRLevel.B1, "b1"),
        (CEFRLevel.B2, "b2"),
        (CEFRLevel.C1, "c1"),
        (CEFRLevel.C2, "c2"),
    ]

    for text, cefr_level in cefr_levels:
        builder.add(
            InlineKeyboardButton(text=text, callback_data=CEFRLevel.get_callback_data(cefr_level))
        )

    builder.adjust(1)
    return builder.as_markup()
