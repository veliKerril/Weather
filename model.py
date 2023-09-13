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




class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def add_user(self, name, email, psw):
        with sq.connect('Weather.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT COUNT() as `count` FROM Users WHERE email LIKE '{email}'")
            res = cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, psw, tm))
        # На самом деле не понятно, хороший это или плохой подход, скорее всего плохой
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM Users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sq.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM Users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sq.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    # Если через self.__cur, то почему-то не происходит коннект с базой данных.
    # В обязательном порядке переписать и разобраться, почему именно так, ведь идейно это совершенно не правильно
    def add_city_with_user_id(self, city, user_id):
        with sq.connect('Weather.db') as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO Location VALUES(NULL, ?, ?)""", (city, user_id))
            print('Все должно быть добавлено')


    def get_cities_by_user_id(self, user_id):
        try:
            self.__cur.execute(f"SELECT name_city FROM Location WHERE userID = '{user_id}'")
            temp = self.__cur.fetchall()
            res = []
            # if not res:
            #     print("Очередная ошибка")
            #     return False
            for city in temp:
                res.append(city['name_city'])
            print(res)
            return res
        except sq.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def del_city_by_user_id(self, user_id, city):
        with sq.connect('Weather.db') as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM Location WHERE userID = '{user_id}' AND name_city = '{city}'")



'''
Да, очень красиво, я до этого не додумался в своих первых проектах, очень красивый именно оопшный паттерн.
То есть в этом классе мы создаем связь с базой данных, получаем как раз курсор, и с ним уже делаем всякое через
функции.
'''

# def get_user_name(self):
#     sql = '''SELECT * FROM Users'''
#     try:
#         self.__cur.execute(sql)
#         res = self.__cur.fetchall()
#         if res:
#             print(res)
#             return res
#     except:
#         print("Ошибка чтения из БД")
#     return []

# def addPost(self, title, text, url):
#     try:
#         self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
#         res = self.__cur.fetchone()
#         if res['count'] > 0:
#             print("Статья с таким url уже существует")
#             return False
#
#         base = url_for('static', filename='images_html')
#
#         text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
#                       "\\g<tag>" + base + "/\\g<url>>",
#                       text)
#
#         tm = math.floor(time.time())
#         self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
#         self.__db.commit()
#     except sq.Error as e:
#         print("Ошибка добавления статьи в БД "+str(e))
#         return False
#
#     return True
#
# def getPost(self, alias):
#     try:
#         self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
#         res = self.__cur.fetchone()
#         if res:
#             return res
#     except sq.Error as e:
#         print("Ошибка получения статьи из БД "+str(e))
#
#     return (False, False)
#
# def getPostsAnonce(self):
#     try:
#         self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
#         res = self.__cur.fetchall()
#         if res: return res
#     except sq.Error as e:
#         print("Ошибка получения статьи из БД "+str(e))
#
#     return []
#
# def addUser(self, name, email, hpsw):
#     try:
#         self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
#         res = self.__cur.fetchone()
#         if res['count'] > 0:
#             print("Пользователь с таким email уже существует")
#             return False
#
#         tm = math.floor(time.time())
#         self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
#         self.__db.commit()
#     except sq.Error as e:
#         print("Ошибка добавления пользователя в БД "+str(e))
#         return False
#
#     return True
#
# def getUser(self, user_id):
#     try:
#         self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
#         res = self.__cur.fetchone()
#         if not res:
#             print("Пользователь не найден")
#             return False
#
#         return res
#     except sq.Error as e:
#         print("Ошибка получения данных из БД "+str(e))
#
#     return False
#
# def getUserByEmail(self, email):
#     try:
#         self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
#         res = self.__cur.fetchone()
#         if not res:
#             print("Пользователь не найден")
#             return False
#
#         return res
#     except sq.Error as e:
#         print("Ошибка получения данных из БД "+str(e))
#
#     return False


if __name__ == '__main__':
    Model.create_bd()
