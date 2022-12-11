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

    def take_table_with_person(self, person):
        self.cur.execute(f"SELECT table_number, person FROM reserve_table "
                         f"WHERE person={person} AND is_reserved != 1 ORDER BY table_number ")
        return self.cur.fetchall()

    def confirmed_reserve(self, table_number):
        self.cur.execute(f"UPDATE reserve_table SET is_reserved = 1 WHERE table_number = {table_number}")
        self.db.commit()