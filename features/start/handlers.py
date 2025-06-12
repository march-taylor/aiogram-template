from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from services.language import LanguageService
from services.messaging import MessagingService
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
	language_code = callback.data.split("_")[1]
	await LanguageService.set_user_language(user_id=callback.from_user.id, language_code=language_code)
	language = await LanguageService.get_user_language(callback.from_user.id)
	
	await state.clear()
	await MessagingService.send_localized(user_id=callback.from_user.id, message_key="language_changed")
	await callback.answer()
	await MessagingService.send_localized(user_id=callback.from_user.id, message_key="welcome")