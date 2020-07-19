# coding=utf-8

from __future__ import absolute_import
import redis
from redis import Redis


class NewRedis(Redis):

    def setex(self, name, time, value):
        """
        重写setex方法
        兼容python2与python3
        :param name:
        :param time:
        :param value:
        :return:
        """
        version, u, v = redis.VERSION
        if int(version) == 2:
            super(NewRedis, self).setex(name, value, time)
        else:
            super(NewRedis, self).setex(name, time, value)


class RedisForSingleton:

    INSTANCE = None

    def __init__(self, **kwargs):
        host = kwargs.get("host")
        port = kwargs.get("port")
        db = kwargs.get("db", 0)
        max_connections = int(kwargs.get("max_connections", 20))
        socket_timeout = int(kwargs.get("socket_timeout", 10))
        socket_connect_timeout = int(kwargs.get("socket_connect_timeout", 5))
        password = kwargs.get("password")
        connection_params = {
            "host": host,
            "port": port,
            "db": db,
            "max_connections": max_connections,
            "password": password,
            "socket_timeout": socket_timeout,
            "socket_connect_timeout": socket_connect_timeout
        }
        pools = redis.ConnectionPool(**connection_params)
        self.redis = NewRedis(connection_pool=pools)

    @classmethod
    def get_instance(cls, redis_config):

        if not RedisForSingleton.INSTANCE:
            init_config = {
                "host": redis_config["host"],
                "port": redis_config["port"],
                "max_connections": redis_config["max_connections"],
                "password": redis_config["password"],
                "db": redis_config["db"]
            }
            RedisForSingleton.INSTANCE = RedisForSingleton(**init_config)
        return RedisForSingleton.INSTANCE


if __name__ == '__main__':
    # redis_config = {
    #     "host": "",
    #     "port": "",
    #     "max_connections": "",
    #     "password": ""
    # }
    pass



