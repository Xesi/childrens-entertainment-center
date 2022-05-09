import sqlite3

#from coursework import db, create_app, models; db.create_all(app=create_app()); user1 = models.User()



connection = sqlite3.connect('database.db')


with open('scripts/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (1, 'Администатор')
)
cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (2, 'учитель английского языка')
)
cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (3, 'тренер по валейболу')
)
cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (4, 'футбольный тренер')
)
cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (5, 'тренер по гимнастике')
)
cur.execute("INSERT INTO positions (id, name) VALUES (?, ?)",
            (6, 'бывший сотрудник')
)


cur.execute("INSERT INTO staff (second_name, first_name, middle_name, user_id, position, admin) VALUES (?, ?, ?, ?, ?, ?)",
            ('Администратор', 'Владимир', 'Владимирович', 3, 1, 1)
)
# cur.execute("INSERT INTO staff (second_name, first_name, middle_name, user_id, position) VALUES (?, ?, ?, ?, ?)",
#             ('Иванова', 'Мария', 'Максимовна', 0, 2)
# )
# cur.execute("INSERT INTO staff (second_name, first_name, middle_name, user_id, position) VALUES (?, ?, ?, ?, ?)",
#             ('Лукин', 'Дмитрий', 'Валерьевич', 0, 3)
# )
# cur.execute("INSERT INTO staff (second_name, first_name, middle_name, user_id, position) VALUES (?, ?, ?, ?, ?)",
#             ('Петров', 'Иван', 'Васильевич', 0, 4)
# )
# cur.execute("INSERT INTO staff (second_name, first_name, middle_name, user_id, position) VALUES (?, ?, ?, ?, ?)",
#             ('Ромашева', 'Нина', 'Дмитриевна', 0, 5)
# )


cur.execute("INSERT INTO types_of_room (name_of_type, max_count_people) VALUES (?, ?)",
            ('Большой спортивный зал', 100)
)
cur.execute("INSERT INTO types_of_room (name_of_type, max_count_people) VALUES (?, ?)",
            ('Малый спортивный зал', 25)
)
cur.execute("INSERT INTO types_of_room (name_of_type, max_count_people) VALUES (?, ?)",
            ('Зал для гимнастики', 20)
)
cur.execute("INSERT INTO types_of_room (name_of_type, max_count_people) VALUES (?, ?)",
            ('Компьютерный класс', 15)
)
cur.execute("INSERT INTO types_of_room (name_of_type, max_count_people) VALUES (?, ?)",
            ('Учебный класс', 25)
)

cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('Спортивный зал 1', 1, 400.0)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('Спортивный зал 2', 2, 250.6)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('Гимнастический зал 1', 3, 101.3)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('101', 4, 50.5)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('102', 4, 61.5)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('103', 4, 56.5)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('104', 5, 36.5)
)
cur.execute("INSERT INTO rooms (name, type_of_room, square_of_room) VALUES (?, ?, ?)",
            ('105', 5, 45.2)
)


cur.execute("INSERT INTO type_of_furniture (name, model, cost) VALUES (?, ?, ?)",
            ('Компьютер преподавателя', 'HP 1', 45000)
)
cur.execute("INSERT INTO type_of_furniture (name, model, cost) VALUES (?, ?, ?)",
            ('Учебный компьютер', 'HP 2', 50000)
)
cur.execute("INSERT INTO type_of_furniture (name, model, cost) VALUES (?, ?, ?)",
            ('Валейбольная сетка', '00000201', 3000)
)
cur.execute("INSERT INTO type_of_furniture (name, model, cost) VALUES (?, ?, ?)",
            ('Проектор', '00000202', 15000)
)


cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (1, 3)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (4, 1)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (4, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (4, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (4, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (5, 1)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (5, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (5, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (5, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (5, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 1)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (6, 2)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (7, 1)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (8, 1)
)
cur.execute("INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)",
            (8, 4)
)


cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Мы открылись!', 'Приглашаем вас к нам на занятия')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('График работы на майских праздниках', 'С 09:00 до 21:00')
            )


connection.commit()
connection.close()