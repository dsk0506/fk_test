# coding:utf-8
import MySQLdb, redis, pymongo, datetime, traceback, sys
from config import config


def db_connect():
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    port = config.get_config('database', 'db_port')
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=name, port=int(port), charset='utf8')
    conn.autocommit(True)
    return conn


db = db_connect()


def redis_connect():
    redis_host = config.get_config('redis', 'host')
    redis_db = config.get_config('redis', 'database')
    redis_port = int(config.get_config('redis', 'port'))
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    return redis_conn


redis_con = redis_connect()


def mongo_connect():
    mongo_host = config.get_config('mongo', 'db_host')
    mongo_port = int(config.get_config('mongo', 'db_port'))
    mongo_client = pymongo.MongoClient(host=mongo_host, port=int(mongo_port))
    return mongo_client


mongo_client = mongo_connect()


def log(name, info):
    filename = '/tmp/log.debug.' + name + '-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    trace = traceback.extract_stack()[-2][:3], str(info)
    output = open(filename, 'a')
    sys.stdout.write(str(info)+'\n')
    with output:
        output.write(str(trace))


# 把json的unicode 转化为字符串
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input