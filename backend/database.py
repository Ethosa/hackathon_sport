# -*- coding: utf-8 -*-
from sqlite3 import connect


db = connect('hackathon_solutions.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    access_token TEXT NOT NULL,
    role INTEGER NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS mark (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    used_language INTEGER NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS lang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    name TEXT NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS default_input (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input TEXT NOT NULL,
    output TEXT NOT NULL
);''')
db.commit()


def default(table: str, min_size: int, values: dict[str, object]):
    roles = cur.execute(f'SELECT * FROM {table}').fetchall()
    if len(roles) < min_size:
        cur.execute(
            f'INSERT INTO {table} ({",".join(values.keys())}) VALUES ({",".join(["?" for i in values.keys()])})',
            tuple(values.values())
        )
        db.commit()


default('role', 2, {'title': 'Пользователь'})  # id = 1
default('role', 2, {'title': 'Администратор'})  # id = 2

default('lang', 3, {'title': 'Python', 'name': 'python'})  # id = 1
default('lang', 3, {'title': 'C#', 'name': 'csharp'})  # id = 2
default('lang', 3, {'title': 'Java', 'name': 'java'})  # id = 3
