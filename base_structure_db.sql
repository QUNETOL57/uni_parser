CREATE TABLE teacher (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
    name        VARCHAR (255) NOT NULL,
    is_tutor    BOOLEAN       NOT NULL
);

CREATE TABLE type (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
    name        VARCHAR (255) NOT NULL
);

INSERT INTO type (id, name) VALUES (1, 'Семинары');
INSERT INTO type (id, name) VALUES (2, 'Лабораторные работы');
INSERT INTO type (id, name) VALUES (3, 'Контрольные работы');
INSERT INTO type (id, name) VALUES (4, 'Курсовые работы');

CREATE TABLE subject (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
    name        VARCHAR (255) NOT NULL,
    semestr     INTEGER       NOT NULL,
    type_id     INTEGER       REFERENCES type (id) ON DELETE CASCADE,
    teacher_id  INTEGER       REFERENCES teacher (id) ON DELETE CASCADE,
    link        VARCHAR (255) NOT NULL
);

CREATE TABLE theme (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
    name        VARCHAR (255) NOT NULL,
    subject_id  INTEGER       REFERENCES subject (id) ON DELETE CASCADE,
    semestr     INTEGER       NOT NULL,
    messages    INTEGER       NOT NULL,
    result      VARCHAR (255) NOT NULL,
    link        VARCHAR (255) NOT NULL
);

CREATE TABLE message (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
    teacher_id  INTEGER       REFERENCES teacher (id) ON DELETE CASCADE,
    subject_id  INTEGER       REFERENCES subject (id) ON DELETE CASCADE,
    theme_id    INTEGER       REFERENCES theme (id) ON DELETE CASCADE,
    my_answer   BOOLEAN       NOT NULL,
    text        TEXT          NOT NULL,
    create_at   DATETIME      NOT NULL
);