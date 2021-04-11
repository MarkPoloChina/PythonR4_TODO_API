# CPR MP FOR W2OL-PY-R4 2021 A.R.R.
import redis
from app import Config
def connect_redis():
    return redis.Redis('127.0.0.1')

def get_redis_data(key):
    conn = connect_redis()
    data = conn.get(key)
    return data

def set_redis_data(key, value):
    conn = connect_redis()
    data = value
    conn.set(
        name=key,
        value=data,
    )

def saveHistory(userId, keyWord):
    conn = connect_redis()
    history = 'history_%s' % userId
    conn.lrem(history, 0, keyWord)
    conn.lpush(history, keyWord)
    conn.ltrim(history, 0, 9)
    return

def getHistory(userId):
    conn = connect_redis()
    history = 'history_%s' % userId
    historyList = conn.lrange(history, 0 ,9)
    listToOutput = list()
    for obj in historyList:
        listToOutput.append(obj.decode())
    return listToOutput