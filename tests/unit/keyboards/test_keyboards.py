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
        assert Language.get_callback_data("english") == "lang_english"
        assert Language.get_callback_data("chinese") == "lang_chinese"

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
        assert button.callback_data == "lang_english"


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
        assert CEFRLevel.get_callback_data("a1") == "cefr_level_a1"
        assert CEFRLevel.get_callback_data("b2") == "cefr_level_b2"

    def test_get_cefr_keyboard_structure(self) -> None:
        """Test CEFR keyboard structure."""
        keyboard = get_cefr_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 6  # 6 levels, adjust(1) - 6 rows

        # Check each row has one button with correct text and callback
        levels = [
            (CEFRLevel.A1, "cefr_level_a1"),
            (CEFRLevel.A2, "cefr_level_a2"),
            (CEFRLevel.B1, "cefr_level_b1"),
            (CEFRLevel.B2, "cefr_level_b2"),
            (CEFRLevel.C1, "cefr_level_c1"),
            (CEFRLevel.C2, "cefr_level_c2"),
        ]

        for i, (expected_text, expected_callback) in enumerate(levels):
            row = keyboard.inline_keyboard[i]
            assert len(row) == 1
            button = row[0]
            assert button.text == expected_text
            assert button.callback_data == expected_callback
