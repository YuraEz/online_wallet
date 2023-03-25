from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)


    def create_new_account_command(self, user_id_tg, nick, age,
                                   user_name_tg, registration_date,
                                   language, money, currency):
        all_users_id = [i[1] for i in self.model.show_full_info()]
        if user_id_tg in all_users_id:
            print("Такой пользователь есть")
            print("")
            return "You already have an account!"
        elif user_id_tg not in all_users_id:
            return self.model.create_new_account_command(user_id_tg, nick, age,
                                                         user_name_tg, registration_date,
                                                         language, money, currency)


    def show_balance(self, user_id_tg):
        user_info = self.model.show_balance(user_id_tg)
        return user_info[0][7], user_info[0][8]


    def top_up_balance(self, user_id_tg, how_much):
        a = self.model.top_up_balance(user_id_tg, how_much+self.model.show_balance(user_id_tg)[0][7])
        print(a)


    def top_down_balance(self, user_id_tg, how_much):
        if self.model.show_balance(user_id_tg)[0][7] - how_much < 0:
            return "There are not enough funds on your balance"
        elif self.model.show_balance(user_id_tg)[0][7] - how_much >= 0:
            self.model.top_down_balance(user_id_tg, self.model.show_balance(user_id_tg)[0][7]-how_much)
            return f"Balance downed up by: {how_much} ZS"


    def get_users(self):
        name = [i[2] for i in self.model.show_full_info()]
        money = [i[7] for i in self.model.show_full_info()]
        return name, money


    def get_nicknames(self, name):
        all_names = [i[2] for i in self.model.show_full_info()]
        if name in all_names:
            return True
        elif name not in all_names:
            return False


    def send_money(self, user_id_tg, how_much, to_who):
        if self.model.show_balance(user_id_tg)[0][7] - how_much < 0:
            return "There are not enough funds on your balance"
        elif self.model.show_balance(user_id_tg)[0][7] - how_much >= 0:
            self.model.top_down_balance(user_id_tg, self.model.show_balance(user_id_tg)[0][7]-how_much)
            self.model.top_up_balance(to_who, how_much+self.model.show_balance(to_who, key=False)[0][7], key=False)
            return f"You sent {how_much} ZS to {to_who}"
