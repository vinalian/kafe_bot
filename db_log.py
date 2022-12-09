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

    def log(self, button, user_id):
        self.cur.execute(f"SELECT * FROM logs LIMIT 1")
        min = self.cur.fetchone()
        self.cur.execute(f"SELECT * FROM logs ORDER BY date_time DESC LIMIT 1 ")
        max = self.cur.fetchone()
        if max[0] - min[0] == 999:
            self.cur.execute(f"DELETE FROM logs WHERE id={min[0]}")
            self.db.commit()
        self.cur.execute(f"INSERT INTO logs (user_id, buttons) VALUES ({user_id}, '{button}')")
        self.db.commit()

    def log_buttons(self, user_id, button_name):
        self.cur.execute(f"INSERT INTO buttons (user_id, button_name) VALUES ({user_id},'{button_name}')")
        self.db.commit()

    def get_menu_name_for_id(self, id):
        self.cur.execute(f"SELECT menu_cat FROM main_menu WHERE id={id}")
        return self.cur.fetchone()

    def get_dish_name_for_id(self, id):
        self.cur.execute(f"SELECT dish FROM menu WHERE id={id}")
        return self.cur.fetchone()

