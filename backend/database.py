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
    task_id INTEGER NOT NULL,
    input TEXT NOT NULL,
    output TEXT NOT NULL,
    hidden BOOLEAN NOT NULL
);''')
db.commit()


def default(table: str, max_size: int, values: dict[str, object]):
    roles = cur.execute(f'SELECT * FROM {table}').fetchall()
    if len(roles) < max_size:
        cur.execute(
            f'INSERT INTO {table} ({",".join(values.keys())}) VALUES ({",".join(["?" for i in values.keys()])})',
            tuple(values.values())
        )
        db.commit()


def defaults(table: str, *values: dict[str, object]):
    for i in values:
        default(table, len(values), i)


defaults(
    'role',
    {'title': 'Пользователь'},  # id = 1
    {'title': 'Администратор'}  # id = 2
)

defaults(
    'lang',
    {'title': 'Python', 'name': 'python'},  # id = 1
    {'title': 'C#', 'name': 'csharp'},  # id = 2
    {'title': 'Java', 'name': 'java'}  # id = 3
)

defaults(
    'task',
    {  # id = 1
        'title': 'Кибербезопасность',
        'description': 'Вы выступаете в роли работника в сфере кибербезопасности. '
                       'Ваша задача - написать программу, которая на вход получает одно единственное слово, '
                       'переводит его на кирпичный язык и выводит полученное слово. '
                       'Особенности кирпичного языка заключаются в том, что после каждой гласной добавляется “с” и эта гласная, '
                       'но если встречается слог, начинающийся с буквы “С”, то перед ним добавляется “у”.\n'
                       'Примеры:\n'
                       'Привет → При + си + ве + се + т → Присивесет\n'
                       'Кусок → Ку + су + у + со + к → Кусуусок\n'
                       'Гулять → Гу + су + ля + ся + ть → Гусулясять',
    }, {  # id = 2
        'title': 'Джун',
        'description': 'Джун Петя получил очередную таску от мидла Васи. '
                       'Петя просит Вас оказать ему помощь в решении этой задачи. '
                       'Суть в том, что пользователь вводит 3 числа, для каждого из которых '
                       'выполняется условие 0 ⩽ x ⩽ 255, где x - число, введенное пользователем. '
                       'Полученные три числа - RGB цвет. '
                       'Программа должна рассчитывать комплементарный (контрастный) цвет указанному, '
                       'после чего вывести его RGB через запятую. Комплементарный цвет - цвет, '
                       'противоположный указанному. Для того, чтобы его посчитать, следует перевести RGB в HSL. '
                       'Формула, по которой следует ориентироваться: H₁ = (H₀ + 180) mod 360.',
    }, {  # id = 3
        'title': 'Аниме',
        'description': 'Ваш друг Олег просит написать для него программу для подсчета '
                       'количества часов просмотренного аниме. Программа должна получать на вход 2 числа x и y. '
                       'x - количество просмотренных серий аниме, y - количество просмотренных полнометражных аниме. '
                       'Одна серия идет 20 минут, а полнометражное аниме идет полтора часа. '
                       'Программа в конце должна вывести только одно число - количество часов, '
                       'округленное в меньшую сторону (например, 2 часа 50 минут нужно считать за 2 часа).',
    }, {  # id = 4
        'title': 'Экзамен',
        'description': 'Вы готовитесь к экзамену по высшей математике, '
                       'однако у Вас есть некоторые проблемы с матрицами, '
                       'поэтому Вашим решением стало написание программ, '
                       'делающих различные операции над матрицами. '
                       'Сейчас Вы должны написать программу, транспонирующую матрицу. '
                       'Программа получает на вход следующие данные: - число N, '
                       'равное размерности матрицы. - N*N-е количество чисел, которыми нужно заполнить матрицу. '
                       'В конце программа должна вывести числа транспонированной матрицы, '
                       'где столбцы разделены одним пробелом, а каждая строка начинается с новой строки.',
    }, {  # id = 5
        'title': 'Факториал',
        'description': 'Дано случайное число n, такое, что 1 ⩽ n ⩽ 100. '
                       'Необходимо написать программу, которая выводит факториал числа n.\n'
                       'Факториал числа  x! = 1 * 2 * 3 * ... * x',
    }, {  # id = 6
        'title': 'Размер имеет значение',
        'description': 'Дано случайное число n, такое, что n ∈ ℕ. '
                       'Необходимо вывести количество цифр в числе n. '
                       'Нельзя переводить число в другие типы данных, например строку. '
                       'Вход: 102030405060\n'
                       'Вывод: 12 ',
    }, {  # id = 7
        'title': 'Работник банка',
        'description': 'Вы являетесь одним из разработчиков банка, '
                       'и Вас попросили сделать программу для шифрования номера карты. '
                       'На вход программа получает x и n, такие, '
                       'что x - это случайный номер карты, а n, такое, что 0 < n < 8.\n'
                       'Программа должна вывести n-е количество звездочек и последние 4 цифры карты, например:\n'
                       'вход: “1234567812345678”, 5\n'
                       'вывод: *****5678',
    }, {  # id = 8
        'title': 'Паскаль',
        'description': 'Даны два случайных числа x и y, для которых существует 0 < x < y < 100. '
                       'Необходимо найти все числа из треугольника Паскаля на отрезке [x; y]. '
                       'Выводить числа следует через запятую без пробелов, в возрастающем порядке.',
    }
)

defaults(
    'default_input',
    {
        'task_id': 1,
        'input': 'Привет',
        'output': 'Присивесет',
        'hidden': False
    }, {
        'task_id': 1,
        'input': 'Как дела?',
        'output': 'Касак деселаса?',
        'hidden': True
    }, {
        'task_id': 1,
        'input': 'По сусекам',
        'output': 'Посо усуусекасам',
        'hidden': True
    }, {
        'task_id': 1,
        'input': 'Сок',
        'output': 'уСок',
        'hidden': False
    }, {
        'task_id': 1,
        'input': 'Я люблю кошек',
        'output': 'Яся Люсюблюсю косошесек',
        'hidden': True
    }, {
        'task_id': 1,
        'input': 'Спортивное программирование',
        'output': 'Спосортисивносоесе просограсаммисиросовасанисиесе',
        'hidden': False
    }, {
        'task_id': 2,
        'input': '223\n19\n127',
        'output': '18,223,114',
        'hidden': False
    }, {
        'task_id': 2,
        'input': '19\n223\n100',
        'output': '223,18,142',
        'hidden': True
    }, {
        'task_id': 2,
        'input': '255\n0\n0',
        'output': '0,255,255',
        'hidden': False
    }, {
        'task_id': 2,
        'input': '19\n56\n116',
        'output': '115,79,19',
        'hidden': True
    }, {
        'task_id': 2,
        'input': '19\n116\n100',
        'output': '115,19,34',
        'hidden': True
    }, {
        'task_id': 3,
        'input': '6\n4',
        'output': '8',
        'hidden': False
    }, {
        'task_id': 3,
        'input': '10\n20',
        'output': '33',
        'hidden': True
    }, {
        'task_id': 3,
        'input': '100\n5',
        'output': '40',
        'hidden': True
    }, {
        'task_id': 3,
        'input': '225\n300',
        'output': '525',
        'hidden': True
    }, {
        'task_id': 3,
        'input': '1280\n720',
        'output': '1506',
        'hidden': True
    }, {
        'task_id': 3,
        'input': '1000\n7',
        'output': '343',
        'hidden': True
    }, {
        'task_id': 4,
        'input': '1\n5',
        'output': '5',
        'hidden': False
    }, {
        'task_id': 4,
        'input': '2\n2\n4\n2\n4',
        'output': '2 2\n4 4',
        'hidden': False
    }, {
        'task_id': 4,
        'input': '2\n5\n1\n3\n2',
        'output': '5 3\n1 2',
        'hidden': False
    }, {
        'task_id': 4,
        'input': '3\n1\n2\n3\n4\n6\n7\n8\n9',
        'output': '1 4 7\n2 5 8\n3 6 9',
        'hidden': True
    }, {
        'task_id': 4,
        'input': '3\n3\n2\n1\n6\n5\n4\n9\n8\n7',
        'output': '3 6 9\n2 5 8\n1 4 7',
        'hidden': True
    }, {
        'task_id': 5,
        'input': '5',
        'output': '120',
        'hidden': False
    }, {
        'task_id': 5,
        'input': '3',
        'output': '6',
        'hidden': False
    }, {
        'task_id': 5,
        'input': '6',
        'output': '720',
        'hidden': False
    }, {
        'task_id': 5,
        'input': '10',
        'output': '3628800',
        'hidden': True
    }, {
        'task_id': 5,
        'input': '14',
        'output': '87178291200',
        'hidden': True
    }, {
        'task_id': 5,
        'input': '8',
        'output': '40320',
        'hidden': True
    }, {
        'task_id': 6,
        'input': '102030405060',
        'output': '12',
        'hidden': False
    }, {
        'task_id': 6,
        'input': '123456',
        'output': '6',
        'hidden': False
    }, {
        'task_id': 6,
        'input': '9128362183',
        'output': '10',
        'hidden': True
    }, {
        'task_id': 6,
        'input': '98137265934',
        'output': '11',
        'hidden': True
    }, {
        'task_id': 6,
        'input': '123',
        'output': '3',
        'hidden': True
    }, {
        'task_id': 6,
        'input': '123123123',
        'output': '9',
        'hidden': True
    }, {
        'task_id': 7,
        'input': '1234123412341234\n2',
        'output': '**1234',
        'hidden': False
    }, {
        'task_id': 7,
        'input': '1234123412341234\n5',
        'output': '*****1234',
        'hidden': False
    }, {
        'task_id': 7,
        'input': '5555192931720022\n4',
        'output': '****0022',
        'hidden': True
    }, {
        'task_id': 7,
        'input': '8263826382739273\n4',
        'output': '****9273',
        'hidden': True
    }, {
        'task_id': 8,
        'input': '1\n3',
        'output': '1,1,1,1,1,2',
        'hidden': False
    }, {
        'task_id': 8,
        'input': '1\n4',
        'output': '1,1,1,1,1,1,1,2,3,3',
        'hidden': False
    }, {
        'task_id': 8,
        'input': '1\n2',
        'output': '1,1,1',
        'hidden': False
    }, {
        'task_id': 8,
        'input': '1\n5',
        'output': '1,1,1,1,1,1,1,1,1,2,3,3,4,4,6',
        'hidden': True
    }, {
        'task_id': 8,
        'input': '3\n6',
        'output': '1,1,1,1,1,1,1,1,2,3,3,4,4,5,5,6,10',
        'hidden': True
    }
)
