from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
def get_main_menu_keyboard():
    buttons = [
        [KeyboardButton(text="👤 Личный кабинет"), KeyboardButton(text="🛠 Методы")],
        [KeyboardButton(text="🔔 Уведомления"), KeyboardButton(text="🆘 Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню Личного Кабинета (НОВОЕ)
def get_cabinet_keyboard():
    buttons = [
        [KeyboardButton(text="💰 Заявка на депозит"), KeyboardButton(text="💸 Заявка на вывод")],
        [KeyboardButton(text="🔗 Загрузить хеш-транзакции")],
        [KeyboardButton(text="⬅️ Назад в главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню Методы (уже было)
def get_methods_keyboard():
    buttons = [
        [KeyboardButton(text="🔄 Внутренний трафик")],
        [KeyboardButton(text="📩 Прием"), KeyboardButton(text="📤 Выплата")],
        [KeyboardButton(text="🚀 Залив"), KeyboardButton(text="🚜 Ферма")],
        [KeyboardButton(text="📦 БТ"), KeyboardButton(text="🌍 Трансгран")],
        [KeyboardButton(text="🤝 Контрагенты")],
        [KeyboardButton(text="⬅️ Назад в главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)