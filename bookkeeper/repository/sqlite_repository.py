"""
Реализация хранения данных посредствам SQL
"""

import sqlite3 as sq
from inspect import get_annotations
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


def make_t_obj(cls: Any, fields: dict[Any, Any], values: str) -> Any:
    """
    Parameters
    ----------
    cls: class of returnable object
    fields: dict of annotations
    values: data from database

    Returns
    -------
    """
    res = object.__new__(cls)  # Создаём объект класса, который будем возвращать
    if values is None:
        return None
    for attr, val in zip(fields.keys(), values):
        # Заполняем его данными из полученной строки из БД
        # print(attr, val)
        setattr(res, attr, val)
    setattr(res, 'pk', values[-1])
    return res


class SQliteRepository(AbstractRepository[T]):
    """
    Class of database with
    Attributes:
        db_file
        table_name
        fields
        cls
    Methods:
        add
        get
        get_all
        get_like
        update
        delete
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        # Словарь аннотаций из класса, который передан
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls

        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            # place holders
            p_holders = ' '.join([f"{field} TEXT," for field in self.fields])
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS "
                f"{self.table_name} ({p_holders} "
                f"pk INTEGER PRIMARY KEY)"
            )
        con.close()

    def add(self, obj: T) -> int:
        if obj.pk != 0:
            raise ValueError('cannot add with pk != 0')
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f"INSERT INTO "
                        f"{self.table_name} ({names}) "
                        f"VALUES({placeholders})", values)
            obj.pk = cur.lastrowid  # type: ignore
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None | Any:
        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE rowid = {pk}")
            res = make_t_obj(self.cls, self.fields, cur.fetchone())
        con.close()
        return res

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(f"SELECT * FROM {self.table_name}")
            else:
                placeholders = " AND ".join([f"{f}=?"
                                             for f in where.keys()])
                values = list(where.values())
                cur.execute(f"SELECT * FROM "
                            f"{self.table_name} "
                            f"WHERE {placeholders}", values)
            values = cur.fetchall()
            res = [make_t_obj(self.cls, self.fields, val) for val in values]
        con.close()
        return res

    def get_like(self, where: dict[str, Any] | None = None) -> list[T]:
        """return list of values that looks like condition in where"""
        if where is None:
            raise ValueError('Where must be not None')
        # function added by power of N_eki 4 ar
        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            placeholders = " AND ".join([f"{f} LIKE ?" for f in where.keys()])
            values = list(where.values())
            cur.execute(f"SELECT * FROM {self.table_name} WHERE {placeholders}", values)
            values = cur.fetchall()
            res = [make_t_obj(self.cls, self.fields, val) for val in values]
        con.close()
        return res

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        names = ', '.join([f"{x} = ?" for x in self.fields.keys()])
        values = [getattr(obj, x) for x in self.fields]

        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE "
                        f"{self.table_name} "
                        f"SET {names} "
                        f"WHERE rowid = {obj.pk}", values)
            obj.pk = cur.lastrowid  # type: ignore
        con.close()

    def delete(self, pk: int) -> None:
        if self.get(pk) is None:
            raise KeyError('this pk doesnt exist')
        with sq.connect(self.db_file, timeout=5) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE rowid = {pk}")
        con.close()
