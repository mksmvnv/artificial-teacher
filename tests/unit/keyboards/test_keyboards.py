from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.language import (
    CEFRLevel,
    Language,
    get_cefr_keyboard,
    get_language_keyboard,
)


class TestLanguageKeyboard:
    """Test language keyboard."""

    def test_language_class_constants(self) -> None:
        """Test Language class constants."""
        assert Language.ENGLISH == "Английский 🇺🇸"

    def test_language_callback_data(self) -> None:
        """Test language callback data generation."""
        assert Language.get_callback_data("EN") == "LANG_EN"
        assert Language.get_callback_data("CN") == "LANG_CN"

    def test_get_language_keyboard_structure(self) -> None:
        """Test language keyboard structure."""
        keyboard = get_language_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1  # adjust(1) - one row

        row = keyboard.inline_keyboard[0]
        assert len(row) == 1  # one button per row

        button = row[0]
        assert isinstance(button, InlineKeyboardButton)
        assert button.text == Language.ENGLISH
        assert button.callback_data == "LANG_EN"


class TestCEFRKeyboard:
    """Test CEFR keyboard."""

    def test_cefr_levels_constants(self) -> None:
        """Test CEFRLevel class constants."""
        assert CEFRLevel.A1 == "A1 🪹"
        assert CEFRLevel.A2 == "A2 🐣"
        assert CEFRLevel.B1 == "B1 🐥"
        assert CEFRLevel.B2 == "B2 🐦"
        assert CEFRLevel.C1 == "C1 🦅"
        assert CEFRLevel.C2 == "C2 🦉"

    def test_cefr_callback_data(self) -> None:
        """Test CEFR callback data generation."""
        assert CEFRLevel.get_callback_data("A1") == "CEFR_A1"
        assert CEFRLevel.get_callback_data("B2") == "CEFR_B2"

    def test_get_cefr_keyboard_structure(self) -> None:
        """Test CEFR keyboard structure."""
        keyboard = get_cefr_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 6  # 6 levels, adjust(1) - 6 rows

        # Check each row has one button with correct text and callback
        levels = [
            (CEFRLevel.A1, "CEFR_A1"),
            (CEFRLevel.A2, "CEFR_A2"),
            (CEFRLevel.B1, "CEFR_B1"),
            (CEFRLevel.B2, "CEFR_B2"),
            (CEFRLevel.C1, "CEFR_C1"),
            (CEFRLevel.C2, "CEFR_C2"),
        ]

        for i, (expected_text, expected_callback) in enumerate(levels):
            row = keyboard.inline_keyboard[i]
            assert len(row) == 1
            button = row[0]
            assert button.text == expected_text
            assert button.callback_data == expected_callback
