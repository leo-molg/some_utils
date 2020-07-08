# coding: utf-8

from aboutRedis import redis_login_util


class ExampleLogin(object):

    def __init__(self, key):
        self.key = key

    def get_token(self):
        redis_conn = redis_login_util.RedisForSingleton.get_instance().redis
        token = redis_conn.get(self.key)
        if token:
            return token
        else:
            login_res = self.login()
            if not login_res:
                return None
            token = login_res["token"]
            try:
                res = redis_conn.set(self.key, token, 10*60)
                if res:
                    print("update token success")
                else:
                    print("update token failed")
            except Exception as e:
                print("cache token into redis error, msg:{}".format(e))
            return token

    def login(self):
        """
        this method is login to other system
        then success can get the token
        else failed get nothing
        :return:
        """
        return {"token": "abc"}



