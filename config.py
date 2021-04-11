import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/todolist?charset=utf8'
    SECRET_KEY = 'WANGCH8131'
    REDIS_DB_URL = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 0
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False