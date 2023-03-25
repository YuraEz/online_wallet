from config import token_tg
from keyboards import kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

class View:
    def __init__(self, controller):
        print("View подключён")
        self.controller = controller


        self.bot = Bot(token=token_tg)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

        class Form(StatesGroup):
            nick = State()
            age = State()
            how_much_up = State()
            how_much_down = State()
            how_much_send = State()
            to_who = State()

        self.info_tg = "Hello, this is a prototype of an online wallet!\n\n" \
                       "To get help write: /help\n" \
                       "To see your balance write: /balance\n" \
                       "To top up balance: /top_up_balance\n" \
                       "To top down balance: /top_down_balance\n" \
                       "To see all users nicknames: /see_users\n" \
                       "To send money: /send_money\n\n" \
                       "Thank you for using our online wallet!"


        @self.dp.message_handler(commands=["start", "help"])
        async def cmd_start(message: types.Message):
            if message.text == "/start":
                await message.reply("Hello, to register in online wallet, create a name:")
                await Form.nick.set()
            elif message.text == "/help":
                await message.answer(self.info_tg)

        @self.dp.message_handler(state=Form.nick)
        async def cmd_nick(message: types.Message, state: FSMContext):
            try:
                if self.controller.get_nicknames(message.text) == False:
                    await state.update_data(nick=message.text)
                    await message.answer("Enter your age: ")
                    await Form.age.set()
                else:
                    raise IndexError
            except IndexError:
                print("Имя занято!")
                await message.answer("A person with that name already exists!\n"
                                     "Try again or enter a different name:")

        @self.dp.message_handler(state=Form.age)
        async def cmd_age(message: types.Message, state: FSMContext):
            try:
                await state.update_data(age=int(message.text))
                name_age = await state.get_data()
                user = await message.reply(f"You are {name_age['nick']}\n"
                                           f"You {name_age['age']} years old",
                                           reply_markup=kb)
                await state.finish()

                register = self.controller.create_new_account_command(message.from_user.id,
                                                           name_age['nick'],
                                                           name_age['age'],
                                                           message.from_user.username,
                                                           user['date'],
                                                           user["reply_to_message"]['from']["language_code"],
                                                           0.00,
                                                           "ZS")

                await message.answer(f"***{register}***\n\n{self.info_tg}")
            except ValueError:
                print("Ошибка")
                await message.answer("It's not a number!\n"
                                     "You need to enter a number!\n"
                                     "\n"
                                     "Enter your age:")


        @self.dp.message_handler(commands=["balance"])
        async def cmd_balance(message: types.Message):
            balance, currency = self.controller.show_balance(message.from_user.id)
            await message.answer(f"Your balance: {balance} {currency}")


        @self.dp.message_handler(commands=["top_up_balance"])
        async def cmd_top_up_balance(message: types.Message):
            await message.answer("You need to enter a number!\n"
                                 "Write how much you need to top up:")
            await Form.how_much_up.set()

        @self.dp.message_handler(state=Form.how_much_up)
        async def cmd_how_much_up(message: types.Message, state: FSMContext):
            try:
                await state.update_data(how_much_up=float(message.text))
                self.controller.top_up_balance(message.from_user.id, float(message.text))
                await message.answer(f"Balance topped up by: {message.text} ZS")
                await state.finish()
            except ValueError:
                print("Ошибка")
                await message.answer("It's not a number!\n"
                                     "You need to enter a number!\n"
                                     "\n"
                                     "Write how much you need to top up:")


        @self.dp.message_handler(commands=["top_down_balance"])
        async def cmd_top_down_balance(message: types.Message):
            await message.answer("You need to enter a number.\nWrite how much you need to top down:")
            await Form.how_much_down.set()

        @self.dp.message_handler(state=Form.how_much_down)
        async def cmd_how_much_down(message: types.Message, state: FSMContext):
            try:
                await state.update_data(how_much_down=float(message.text))
                string = self.controller.top_down_balance(message.from_user.id, float(message.text))
                await message.answer(string)
                await state.finish()
            except ValueError:
                print("Ошибка")
                await message.answer("It's not a number!\n"
                                     "You need to enter a number!\n"
                                     "\n"
                                     "Write how much you need to top down:")


        @self.dp.message_handler(commands=["see_users"])
        async def cmd_see_users(message: types.Message):
            name, money = self.controller.get_users()
            for i in range(0, len(name)):
                await message.answer(f"{name[i]}: {money[i]}")


        @self.dp.message_handler(commands=["send_money"])
        async def send_money(message: types.Message):
            await message.answer("Enter the nickname of the person you want to send money:")
            await Form.to_who.set()

        @self.dp.message_handler(state=Form.to_who)
        async def cmd_to_who(message: types.Message, state: FSMContext):
            try:
                if self.controller.get_nicknames(message.text):
                    await state.update_data(to_who=message.text)
                    await message.answer("Enter how much you need to send:")
                    await Form.how_much_send.set()
                else:
                    raise IndexError
            except IndexError:
                print("Такого пользователя не существует")
                await message.answer("User with this name does not exist.\n"
                                     "Check if you have written correctly.\n"
                                     "Try again:")

        @self.dp.message_handler(state=Form.how_much_send)
        async def cmd_how_much(message: types.Message, state: FSMContext):
            try:
                await state.update_data(how_much_send=float(message.text))
                name_how_much = await state.get_data()
                string = self.controller.send_money(message.from_user.id,
                                                    name_how_much['how_much_send'],
                                                    name_how_much['to_who'])
                await message.answer(string)
                await state.finish()
            except ValueError:
                print("Ошибка цифр")
                await message.answer("It's not a number!\n"
                                     "You need to enter a number!\n"
                                     "\n"
                                     "Enter how much you want to send:")


        @self.dp.message_handler()
        async def echo_send(message: types.Message):
            await message.answer(message.text)


        executor.start_polling(self.dp, skip_updates=True)
