import sqlite3 as sq
import math
import time

class Model:
    @staticmethod
    def create_bd():
        with sq.connect('Weather.db') as con:
            cur = con.cursor()

            cur.execute("""DROP TABLE IF EXISTS Users""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            time INTEGER NOT NULL
            )""")

            cur.execute("""DROP TABLE IF EXISTS Location""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Location (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name_city TEXT NOT NULL,
            userID INTEGER,
            FOREIGN KEY(userID) REFERENCES Users(ID)
            )""")

    @staticmethod
    def add_user(name, email, psw):
        with sq.connect('Weather.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT COUNT() as `count` FROM Users WHERE email LIKE '{email}'")
            res = cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, psw, tm))


if __name__ == '__main__':
    Model.create_bd()
