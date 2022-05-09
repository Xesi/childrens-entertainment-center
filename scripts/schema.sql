DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    second_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    user_id INTEGER,
    position INTEGER,
    admin BOOLEAN,
    FOREIGN KEY (position) REFERENCES positions(id)
);


DROP TABLE IF EXISTS positions;
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);


DROP TABLE IF EXISTS rooms;
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type_of_room TEXT NOT NULL,
    square_of_room REAL,
    FOREIGN KEY (type_of_room) REFERENCES types_of_room(id_of_type)
);


DROP TABLE IF EXISTS types_of_room;
CREATE TABLE types_of_room (
    id_of_type INTEGER PRIMARY KEY AUTOINCREMENT,
    name_of_type TEXT NOT NULL,
    max_count_people INTEGER
);


DROP TABLE IF EXISTS furniture_and_electronics;
CREATE TABLE furniture_and_electronics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number_of_room INTEGER,
    type INTEGER,
    FOREIGN KEY (number_of_room) REFERENCES rooms(room)
    FOREIGN KEY (type) REFERENCES type_of_furniture(furniture_id)
);


DROP TABLE IF EXISTS type_of_furniture;
CREATE TABLE type_of_furniture (
    furniture_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    cost INTEGER
);


DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);


DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher INTEGER,
    room INTEGER,
    r_date DATE,
    time_start time,
    time_end time,
    cost int,
    max_persons integer,

    FOREIGN KEY (teacher) REFERENCES staff(id),
    FOREIGN KEY (room) REFERENCES rooms(id)
);


DROP TABLE IF EXISTS reserves;
CREATE TABLE reserves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event INTEGER,
    person INTEGER,

    FOREIGN KEY (event) REFERENCES events(id)
);

