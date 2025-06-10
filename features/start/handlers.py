from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n.middleware import I18nMiddleware

from .keyboards import language_keyboard
from .service import StartService
from .states import RegistrationStates


router = Router()
service = StartService()

@router.message(F.text == "/start")
async def start_command(
	message: Message,
	state: FSMContext,
	i18n: I18nMiddleware,
	user: dict | None
):
	if user:  # Пользователь уже есть в БД
		await message.answer(i18n.gettext("welcome", locale=user['language']))
	else:	 # Новый пользователь
		await state.set_state(RegistrationStates.select_language)
		await message.answer(
			i18n.gettext("choose_language"),
			reply_markup=language_keyboard()
		)

@router.callback_query(F.data.startswith("lang_"), RegistrationStates.select_language)
async def set_language(
	callback: CallbackQuery,
	state: FSMContext,
	i18n: I18nMiddleware
):
	lang_code = callback.data.split("_")[1]
	
	# Добавление пользователя в базу данных
	from database.users import UserRepository
	user_repo = UserRepository()
	await user_repo.add_user(callback.from_user.id, lang_code)
	
	await state.clear()
	await callback.message.edit_text(i18n.gettext("language_changed", locale=lang_code))
	await callback.answer()
	await callback.message.answer(i18n.gettext("welcome", locale=lang_code))