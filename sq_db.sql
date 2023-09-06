DROP TABLE IF EXISTS Users;
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
time INTEGER NOT NULL
);
DROP TABLE IF EXISTS Location;
CREATE TABLE IF NOT EXISTS Location (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name_city TEXT NOT NULL,
userID INTEGER,
FOREIGN KEY(userID) REFERENCES Users(ID)
);