# coding: utf-8

"""
the example how to use the mysql util
env: python + django
"""
from aboutMysql import mysql_util as mysql
from django.conf import settings


# example query on crow
def get_one_data(tb_name, k, v, **kwargs):
    """

    :param tb_name:
    :param k:
    :param v:
    :param kwargs:
    :return: dict
    """
    ins = mysql.Mysql.get_instance(settings.DB_NAME)
    conn = ins.get_connection()
    args = []
    sql = '''SELECT * FROM {} WHERE {}=%s'''.format(tb_name, k)
    args.append(v)
    if kwargs:
        for key, value in kwargs.items():
            sql += " and {}=%s".format(key)
            args.append(value)
    # return sql, args
    return ins.query_one(conn, sql, args)


def get_more_data(tb_name, k, v, limit=None, **kwargs) -> list:
    """

    :param tb_name: database table name
    :param k: key
    :param v: value
    :param limit:
    :param kwargs:
    :return: list
    """
    ins = mysql.Mysql.get_instance(settings.DB_NAME)
    conn = ins.get_connection()
    args = []
    sql = '''SELECT * FROM {} WHERE {}=%s'''.format(tb_name, k)
    args.append(v)
    if kwargs:
        for key, value in kwargs.items():
            sql += " and {}=%s".format(key)
            args.append(value)
    if limit:
        sql += " limit %s"
        args.append(limit)
    # return sql, args
    return ins.query(conn, sql, args)


def simple_insert(tb_name, insert_data):
    """

    :param tb_name:
    :param insert_data: dict
    :return:
    """
    ins = mysql.Mysql.get_instance(settings.DB_NAME)
    conn = ins.get_connection()
    return ins.simple_insert(tb_name, insert_data, conn)


def simple_update_table(tb_name, where_data, update_data):
    """

    :param tb_name:
    :param where_data: dict
    :param update_data: dict
    :return:
    """
    ins = mysql.Mysql.get_instance(settings.DB_NAME)
    conn = ins.get_connection()
    return ins.simple_update(tb_name, update_data, where_data, conn)


def query_eq_neq(tb_name, eq=None, neq=None, more=None):
    ins = mysql.Mysql.get_instance(settings.DB_NAME)
    conn = ins.get_connection()
    sql = '''select * from {}'''.format(tb_name)
    args = []
    if eq:
        for k, v in eq.items():
            if "where" in sql:
                sql += " and {}=%s".format(k)
            else:
                sql += " where {}=%s".format(k)
            args.append(v)
    if neq:
        for k, v in neq.items():
            if "where" in sql:
                sql += " and {}!=%s".format(k)
            else:
                sql += " where {}!=%s".format(k)
            args.append(v)
    if more:
        return ins.query(conn, sql, args)
    return ins.query_one(conn, sql, args)


if __name__ == "__main__":
    table = "tb_person"
    query_key = "name"
    query_value = "susan"
    args_dict = {
        "class": "2",
        "age": 18
    }
    lim = "4,10"
    # sqls, arg = get_more_data(table, query_key, query_value, lim, **args_dict)
    # print(sqls % tuple(arg))






