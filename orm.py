import sqlite3

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS educators (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name     VARCHAR (255) NOT NULL,
    subject  VARCHAR (255) NOT NULL,
    semestr  INTEGER (2)   NOT NULL,
    is_tutor BOOLEAN       NOT NULL
  )""")

    

cursor.execute("""INSERT INTO educators (name, subject, semestr, is_tutor)
                  VALUES ('Котло Степан Александрович', 'Баскетбол', 4, false)""")

connect.commit()