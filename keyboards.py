from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/help")
b2 = KeyboardButton("/balance")
b3 = KeyboardButton("/top_up_balance")
b4 = KeyboardButton("/top_down_balance")
b5 = KeyboardButton("/see_users")
b6 = KeyboardButton("/send_money")

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(b1, b2).row(b3, b4).row(b5, b6)