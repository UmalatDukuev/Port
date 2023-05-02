from typing import Tuple, List
from db_context_manager import DBConnection


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def select_dict(dbconfig: dict, _sql: str):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        result = []
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

        return result


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            print('args= ', arg)
            param_list.append(arg)
        print('param_list= ', param_list)
        res = cursor.callproc(proc_name, param_list)
        print(res)

        return res
