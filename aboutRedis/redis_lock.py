# coding:utf-8
import time
from aboutRedis import redis_login_util

init_config = {
            "host": "",
            "port": "",
            "max_connections": "",
            "password": "",
            "db": 0
        }


def get_lock(redis_key, expire_seconds):
    redis_conn = redis_login_util.RedisForSingleton.get_instance(init_config).redis
    ret = redis_conn.setnx(redis_key, 1)
    if ret:
        redis_conn.expire(redis_key, expire_seconds)
        return 0
    else:
        return -1


def remove_lock(redis_key):
    redis_conn = redis_login_util.RedisForSingleton.get_instance(init_config).redis
    ret = redis_conn.delete(redis_key)
    if ret:
        return 0
    else:
        return -1


def example_use():

    while get_lock("redis_key", 60) == -1:
        time.sleep(1)

    # do something
    try:
        pass
    except Exception as e:
        # raise exception remove the lock
        remove_lock("redis_key")
        
    # final remove the lock
    remove_lock("redis_key")


if __name__ == "__main__":
    print(get_lock('new', expire_seconds=60))
    # print remove_lock('new')
