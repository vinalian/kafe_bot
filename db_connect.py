import psycopg2


DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = '9362'
HOST = 'localhost'
PORT = '8000'


class Connect:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def register_new_user(self, user_id, user_name):
        self.cur.execute(f"INSERT INTO user_data (user_id, user_name) VALUES ({user_id}, '{user_name}')")
        self.db.commit()

    def get_dish_name_byID(self, id):
        self.cur.execute(f"SELECT menu_cat FROM main_menu WHERE id={id}")
        return self.cur.fetchall()

    def get_cut_id_byName(self, cat_name):
        self.cur.execute(f"SELECT cat_id FROM menu WHERE dish='{cat_name}'")
        return self.cur.fetchall()

    def main_menu(self):
        self.cur.execute(f"SELECT id, menu_cat FROM main_menu")
        return self.cur.fetchall()

    def menu(self, menu_cat):
        self.cur.execute(f"SELECT id, dish FROM menu WHERE cat_id={menu_cat}")
        return self.cur.fetchall()

    def get_item_info(self, id):
        self.cur.execute(f"SELECT dish, price, weight, description, image_id FROM menu WHERE id={id}")
        return self.cur.fetchall()
