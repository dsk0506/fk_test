# coding:utf-8
import pytest
import MySQLdb
import redis
import pymongo
import os
from config import config


def db_init():
    '''
    数据库表数据清空
    :return:
    '''
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    port = config.get_config('database', 'db_port')
    #mysql_conn = 'mysql -h %s -u%s -p%s -P%s ' %(host,user,passwd,port)
    mysql_conn = 'mysql -h %s -u%s -P%s ' % (host, user, port)
    init_shell = mysql_conn+' -N -s information_schema -e ' + '\"SELECT CONCAT(\'TRUNCATE TABLE \',TABLE_NAME,\';\') FROM TABLES WHERE TABLE_SCHEMA=\''+ name + '\'\"'+'|' +mysql_conn + ' -f '+ name
    print init_shell
    #os.system(init_shell)
    print "这里面数据库初始化"

db_init()
def mongo_init():
    '''
    mongo初始化
    :return:
    '''
    mongo_host = config.get_config('mongo', 'db_host')
    mongo_db = config.get_config('mongo', 'db_name')
    mongo_port = int(config.get_config('mongo', 'db_port'))
    mongo_conn = 'mongo %s:%s/%s' %(mongo_host,mongo_port,mongo_db)
    init_shell = mongo_conn+" --quiet --eval 'db.dropDatabase();'"
    print init_shell
    os.system(init_shell)
    print "这里面mongo初始化"


def redis_init():
    '''
    redis清空
    :return:
    '''
    redis_host = config.get_config('redis', 'host')
    redis_db = config.get_config('redis', 'database')
    redis_port = int(config.get_config('redis', 'port'))
    redis_shell = 'redis-cli -h %s -p %s -n %s' %(redis_host,redis_port,redis_db)
    init_shell = redis_shell+' KEYS "*" | xargs '+redis_shell+' DEL'
    os.system(init_shell);
    print "这里面redis初始化"


@pytest.fixture(scope="session", autouse=True)
def data_init():
    db_init()
    mongo_init()
    redis_init()
    print "这里面数据初始化初始化"


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
def redis_cur():
    redis_host = config.get_config('redis', 'host')
    redis_db = config.get_config('redis', 'database')
    redis_port = int(config.get_config('redis', 'port'))
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    return redis_conn


@pytest.fixture(scope="function")
def mongo_cur(request):
    def fin():
        if mongo_client:
            mongo_client.close()

    request.addfinalizer(fin)
    mongo_host = config.get_config('mongo', 'db_host')
    mongo_db = config.get_config('mongo', 'db_name')
    mongo_port = int(config.get_config('mongo', 'db_port'))
    mongo_client = pymongo.MongoClient(host=mongo_host, port=int(mongo_port))
    mongo_conn = mongo_client[mongo_db]
    return mongo_conn
