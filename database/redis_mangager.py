# -*- coding:utf-8 -*-
import redis
import configparser

class RedisDB:
    def __init__(self):
        self.__config('redis')

    def __config(self, section):
        conf = configparser.ConfigParser()
        conf.read("./Config/db.conf")
        self.__host = conf.get(section, 'host')
        self.__port = int(conf.get(section, 'port'))
        self.__db = int(conf.get(section, 'db'))
        self.__password=int(conf.get(section,'password'))
        self._connect()

    def _connect(self):
        self._redis = redis.Redis(host=self.__host, port=self.__port, db=self.__db,password=self.__password)
        return self._redis

    def selectDB(self, db):
        self.__db = db
        self._connect()
        return self

    def selectConfig(self, section):
        self.__config(section)
        return self

    def decode(self, val):
        if isinstance(val, dict):
            temp = {}
            for k, v in val.items():
                temp[k.decode()] = v.decode()
            val = temp
        elif isinstance(val, list):
            temp = []
            for v in val:
                temp.append(v.decode())
            val = temp
        elif isinstance(val, set):
            temp = []
            for v in val:
                temp.append(v.decode())
            val = set(temp)
        elif val:
            val = val.decode()
        return val

    # key => value 键值对
    def set(self, name, value=None, ex=None, px=None, nx=False, xx=False):
        if isinstance(name, dict):
            if not px:
                px = False
            return self._redis.mset(name, value, ex, px, nx)
        else:
            return self._redis.set(name, value, ex, px, nx, xx)

    def get(self, name):
        if isinstance(name, list):
            res = self.decode(self._redis.mget(name))
        else:
            res = self.decode(self._redis.get(name))
        return res

    def incr(self, name, amount=1):
        return self._redis.incr(name, amount)

    def decr(self, name, amount=1):
        return self._redis.decr(name, amount)

    def delete(self, *names):
        return self._redis.delete(*names)

    def expire(self, name, time=0):
        return self._redis.expire(name, time)

    def exists(self, name):
        return self._redis.exists(name)

    def move(self, name, db):
        return self._redis.move(name, db)

    def keys(self, pattern='*'):
        return self._redis.keys(pattern)

    def type(self, name):
        return self._redis.type(name)

    # hash 哈希数组
    def hset(self, name, key=None, value=None):
        if isinstance(key, dict):
            return self._redis.hmset(name, key)
        else:
            return self._redis.hset(name, key, value)

    def hget(self, name, key=None):
        if isinstance(key, list):
            return self.decode(self._redis.hmget(name, key))
        elif key:
            return self.decode(self._redis.hget(name, key))
        else:
            return self.decode(self._redis.hgetall(name))

    def hincrby(self, name, key, amount=1):
        return self._redis.hincrby(name, key, amount)

    def hscan(self, name, cursor=0, match=None, count=None):
        cursor, data = self._redis.hscan(name, cursor, match, count)
        return (cursor, self.decode(data))

    def hdel(self, name, *keys):
        return self._redis.hdel(name, *keys)

    # list 队列
    def lpush(self, name, *values):
        return self._redis.lpush(name, *values)

    def rpush(self, name, *values):
        return self._redis.rpush(name, *values)

    def linsert(self, name, where, refvalue, value):
        return self._redis.linsert(name, where, refvalue, value)

    def lset(self, name, index, value):
        return self._redis.lset(name, index, value)

    def lindex(self, name, index=0):
        return self.decode(self._redis.lindex(name, index))

    def llen(self, name):
        return self._redis.llen(name)

    def lrange(self, name, offset=0, limit=-1):
        return self.decode(self._redis.lrange(name, offset, limit))

    def lrem(self, name, value, num=0):
        return self._redis.lrem(name, value, num)

    def ltrim(self, name, start=0, end=-1):
        return self._redis.ltrim(name, start, end)

    def lpop(self, name):
        return self.decode(self._redis.lpop(name))

    def rpop(self, name):
        return self.decode(self._redis.rpop(name))

    # set 集合
    def sadd(self, name, *values):
        return self._redis.sadd(name, *values)

    def smembers(self, name):
        return self.decode(self._redis.smembers(name))

    def scard(self, name):
        return self._redis.scard(name)

    def spop(self, name):
        return self.decode(self._redis.spop(name))

    def srem(self, name, *values):
        return self._redis.srem(name, *values)

    # zset 有序集合
    def zadd(self, name, *args):
        return self._redis.zadd(name, *args)

    def zrange(self, name, start=0, end=-1, desc=False, withscores=False, score_cast_func=float):
        return self._redis.zrange(name, start, end, desc, withscores, score_cast_func)

    def zcard(self, name):
        return self._redis.zcard(name)