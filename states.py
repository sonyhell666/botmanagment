from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    waiting_for_data = State()
    waiting_for_video = State()
    main_menu = State()
    
    # Финансы
    waiting_for_deposit_amount = State()
    
    # Раздельный вывод
    waiting_for_withdraw_amount = State()
    waiting_for_withdraw_wallet = State()