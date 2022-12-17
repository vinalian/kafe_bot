import psycopg2


DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = '9362'
HOST = 'localhost'
PORT = '8000'


class Connect_menu:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def if_superuser(self, user_id):
        self.cur.execute(f"SELECT is_superuser FROM user_data WHERE user_id={user_id}")
        return self.cur.fetchone()

    def create_new_cat(self, cat_name, disc):
        self.cur.execute(f"INSERT INTO main_menu(menu_cat, description) VALUES ('{cat_name}', '{disc}')")
        self.db.commit()

    def delete_cat(self, cat_id):
        self.cur.execute(f"DELETE FROM main_menu WHERE id={cat_id}")
        self.db.commit()

    def select_cat(self, cat_name):
        self.cur.execute(f"SELECT id FROM main_menu WHERE id={cat_name}")
        return self.db.commit()

    def delete_dish(self, dish_id):
        self.cur.execute(f"DELETE FROM menu WHERE id={dish_id}")
        self.db.commit()

    def add_new_dish(self, dish, price, weight, cat_id, desc, image_id):
        self.cur.execute(f"INSERT INTO menu(dish, price, weight, cat_id, description, image_id) VALUES ('{dish}',{price},{weight}, {cat_id}, '{desc}','{image_id}')")
        self.db.commit()


class Connect_log:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def get_buttons_top(self):
        self.cur.execute(f"SELECT button_name, COUNT(button_name) FROM buttons WHERE date_time > DATE(now() - interval '7 day') GROUP BY button_name ORDER BY count DESC LIMIT 5")
        return self.cur.fetchall()

    def get_users_top(self):
        self.cur.execute(f"SELECT user_id, COUNT(user_id) FROM buttons GROUP BY user_id ORDER BY count DESC LIMIT 3")
        return self.cur.fetchall()

    def get_user_name_byID(self, user_id):
        self.cur.execute(f"SELECT user_name FROM user_data WHERE user_id={user_id}")
        return self.cur.fetchone()

    def take_logs(self):
        self.cur.execute("SELECT * FROM logs")
        return self.cur.fetchall()


class Connect_superuser:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def give_superuser(self, user_name):
        self.cur.execute(f"UPDATE user_data SET is_superuser = '1' WHERE user_name='{user_name}'")
        self.db.commit()

    def select_all_superuser(self):
        self.cur.execute(f"SELECT user_name FROM user_data WHERE is_superuser='1'")
        return self.cur.fetchall()


    def del_superuser(self, user_name):
        self.cur.execute(f"UPDATE user_data SET is_superuser = '0' WHERE user_name='{user_name}'")
        self.db.commit()


class Connect_reserve:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def cansel_all_reserve(self):
        self.cur.execute(f"UPDATE reserve_table SET is_reserved = 0 WHERE is_reserved = 1")
        self.db.commit()

    def cancel_reserve(self, table_number):
        self.cur.execute(f"UPDATE reserve_table SET is_reserved = 0 WHERE table_number = {table_number}")
        self.db.commit()

    def get_reserve_table(self):
        self.cur.execute(f"SELECT table_number FROM reserve_table WHERE is_reserved = 1")
        return self.cur.fetchall()
