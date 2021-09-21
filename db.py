import sqlite3
from typing import Dict, List, Tuple, Union

DB_NAME = 'uni_base.db'

connect = sqlite3.connect(DB_NAME)
cursor = connect.cursor()

def feach(table: str, columns: Union[list,str] = '*') -> List[Tuple]:
    cursor.execute(f"SELECT {columns} FROM {table}")
    return cursor.fetchall()

def feach_all(table: str, columns_value: Dict) -> Tuple:
    _feach_part(table, columns_value)
    return cursor.fetchall()

def feach_one(table: str, columns_value: Dict) -> Tuple:
    _feach_part(table, columns_value)
    return cursor.fetchone()

def _feach_part(table: str, columns_value: Dict):
    where_part = ''
    for column, value in columns_value.items():
        where_part += f"{column}='{value}'"

    cursor.execute(f"SELECT * FROM {table} WHERE " + where_part)


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    connect.commit()

def get_cursor():
    return cursor

def _init_db():
    """Инициализирует БД"""
    with open('base_structure_db.sql', 'r') as file:
        sql = file.read()
    cursor.executescript(sql)
    connect.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teacher'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()       