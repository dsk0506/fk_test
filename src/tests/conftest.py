# coding:utf-8
import pytest
from config import config
from common import db, redis_con, mongo_client
import init


@pytest.fixture(scope="session", autouse=True)
def data_init():
    init.db_init()
    init.mongo_init()
    init.redis_init()
    init.user_init()
    print "初始化完成"


@pytest.fixture(scope="function")
def cur(request):
    def fin():
        if db_cur:
            db_cur.close()
            db.close()

    #request.addfinalizer(fin)
    db_cur = db.cursor()
    return db_cur


@pytest.fixture(scope="function")
def redis_cur():
    return redis_con


@pytest.fixture(scope="function")
def mongo_cur(request):
    def fin():
        if mongo_client:
            mongo_client.close()

    request.addfinalizer(fin)
    mongo_db = config.get_config('mongo', 'db_name')
    mongo_conn = mongo_client[mongo_db]
    return mongo_conn
