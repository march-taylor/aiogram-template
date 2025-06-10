from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_keyboard():
	builder = InlineKeyboardBuilder()
	builder.button(text="🇬🇧 English", callback_data="lang_en")
	builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
	builder.adjust(2)
	return builder.as_markup()