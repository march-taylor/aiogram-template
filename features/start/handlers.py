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
	user: dict | None,
	_: callable  # Функция перевода
):
	if user:  # Пользователь уже есть в БД
		await message.answer(_("welcome"))
	else:	 # Новый пользователь
		await state.set_state(RegistrationStates.select_language)
		await message.answer(
			_("choose_language"),
			reply_markup=language_keyboard()
		)

@router.callback_query(F.data.startswith("lang_"), RegistrationStates.select_language)
async def set_language(
	callback: CallbackQuery,
	state: FSMContext,
	_: callable
):
	lang_code = callback.data.split("_")[1]
	
	from database.users import UserRepository
	user_repo = UserRepository()
	await user_repo.add_user(callback.from_user.id, lang_code)
	
	await state.clear()
	await callback.message.edit_text(_("language_changed"))
	await callback.answer()
	await callback.message.answer(_("welcome"))