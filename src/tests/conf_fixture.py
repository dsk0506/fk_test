import MySQLdb
import pymongo
import pytest
import redis
from config import config


@pytest.fixture(scope="function")
def cur(request):
    def fin():
        if db_cur:
            db_cur.close()
            conn.close()

    request.addfinalizer(fin)
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    port = config.get_config('database', 'db_port')
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=name, port=int(port))
    db_cur = conn.cursor()
    return db_cur


@pytest.fixture(scope="function")
def redis_cur(request):
    def fin():
        if redis_conn:
            redis_conn.shutdown()

    request.addfinalizer(fin)
    redis_host = config.get_config('redis', 'host')
    redis_db = config.get_config('redis', 'database')
    redis_port = int(config.get_config('redis', 'port'))
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    return redis_conn


def mongo_cur():
    mongo_host = config.get_config('mongo', 'db_host')
    mongo_db = config.get_config('mongo', 'db_name')
    mongo_port = int(config.get_config('mongo', 'db_port'))
    mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
    mongo_conn = mongo_client.mongo_db
    return mongo_conn
