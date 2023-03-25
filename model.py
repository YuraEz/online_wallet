import sqlalchemy as db

class Model:
    def __init__(self):
        print("База данных есть")
        self.engine = db.create_engine("sqlite:///online_wallet.db")
        self.connection = self.engine.connect()
        metadata = db.MetaData()
        self.user_info = db.Table("user_info", metadata,
                                  db.Column("id", db.Integer, primary_key=True),
                                  db.Column("user_id_tg", db.Integer),
                                  db.Column("user_nick", db.Text),
                                  db.Column("user_age", db.Integer),
                                  db.Column("user_name_tg", db.Text),
                                  db.Column("registration_date", db.Text),
                                  db.Column("language", db.Text),
                                  db.Column("money", db.Float),
                                  db.Column("currency", db.Text))
        metadata.create_all(self.engine)


    def show_balance(self, user_id_tg_or_nick_name, key=True):
        if key:
            select_query = db.select(self.user_info)\
                .where(self.user_info.columns.user_id_tg == user_id_tg_or_nick_name)
        else:
            select_query = db.select(self.user_info)\
                .where(self.user_info.columns.user_nick == user_id_tg_or_nick_name)

        select_result = self.connection.execute(select_query)
        return select_result.fetchall()


    def top_up_balance(self, user_id_tg_or_nick_name, how_much, key=True):
        if key:
            update_query = db.update(self.user_info)\
                .where(self.user_info.columns.user_id_tg == user_id_tg_or_nick_name)\
                .values(money=how_much)
        else:
            update_query = db.update(self.user_info)\
                .where(self.user_info.columns.user_nick == user_id_tg_or_nick_name)\
                .values(money=how_much)

        self.connection.execute(update_query)
        self.connection.commit()
        return "Успешно пополнено"


    def top_down_balance(self, user_id_tg, how_much):
        update_query = db.update(self.user_info)\
            .where(self.user_info.columns.user_id_tg == user_id_tg)\
            .values(money=how_much)

        self.connection.execute(update_query)
        self.connection.commit()


    def delete_line(self):
        delete_query = db.delete(self.user_info).where(self.user_info.columns.id == 10)
        self.connection.execute(delete_query)
        self.connection.commit()


    def show_full_info(self):
        select_query = db.select(self.user_info)
        select_result = self.connection.execute(select_query)
        return select_result.fetchall()


    def create_new_account_command(self, user_id_tg, nick, age,
                                   user_name_tg, registration_date,
                                   language, money, currency):
        insert_query = self.user_info.insert().values([
            {"user_id_tg": user_id_tg,
             "user_nick": nick,
             "user_age": age,
             "user_name_tg": user_name_tg,
             "registration_date": registration_date,
             "language": language,
             "money": money,
             "currency": currency}
        ])
        self.connection.execute(insert_query)
        self.connection.commit()

        for i in self.show_full_info():
            print(i)

        return "You have successfully registered"
