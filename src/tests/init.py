# coding:utf-8
from config import config
import os, requests, time, json
import global_params
from  common import redis_con, db


def db_init():
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    port = config.get_config('database', 'db_port')
    # mysql_conn = 'mysql -h %s -u%s -p%s -P%s ' %(host,user,passwd,port)
    mysql_conn = 'mysql -h %s -u%s -P%s ' % (host, user, port)
    init_shell = mysql_conn + ' -N -s information_schema -e ' + '\"SELECT CONCAT(\'TRUNCATE TABLE \',TABLE_NAME,\';\') FROM TABLES WHERE TABLE_SCHEMA=\'' + name + '\'\"' + '|' + mysql_conn + ' -f ' + name
    # print init_shell
    os.system(init_shell)
    print "这里面数据库初始化"


def mongo_init():
    '''
    mongo初始化
    :return:
    '''
    mongo_host = config.get_config('mongo', 'db_host')
    mongo_db = config.get_config('mongo', 'db_name')
    mongo_port = int(config.get_config('mongo', 'db_port'))
    mongo_conn = 'mongo %s:%s/%s' % (mongo_host, mongo_port, mongo_db)
    init_shell = mongo_conn + " --quiet --eval 'db.dropDatabase();db.counter.insert({_id:\"apply_id\",req:NumberLong(0)});db.counter.insert({_id:\"serial_no\",req:NumberLong(0)})'"
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
    redis_shell = 'redis-cli -h %s -p %s -n %s' % (redis_host, redis_port, redis_db)
    init_shell = redis_shell + ' KEYS "*" | xargs ' + redis_shell + ' DEL'
    os.system(init_shell);
    print "这里面redis初始化"


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


def user_init():
    phone = config.get_config('app', 'phone')
    url = config.get_config('app', 'host') + '/ucenter/captcha/company_trial'
    data = {'telephone': phone}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}
    res = requests.post(url, data=data, headers=headers)
    expact_data = {
        "status": 0,
        "message": "验证码已发送",
        "data": []
    }
    assert byteify(json.loads(res.text)) == expact_data
    captcha = redis_con.hgetall('COMPANY_TRIAL' + phone)
    print "验证码:" + captcha['code']
    url = config.get_config('app', 'host') + '/ucenter/company/create'
    principal = "丁守坤"
    data = {'fullname_zh': "全程费控公司", 'principal': principal, 'telephone': phone, 'code': captcha['code'],
            'email': '393573645%40qq.com', 'shortname': '费控', 'license': ''}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0', 'X-From': 'www'}
    requests.post(url, data=data, headers=headers)
    print  "休息下让队列跑一会"
    time.sleep(15)
    url = config.get_config('app', 'host') + '/ucenter/login'
    data = {'username': str(phone), "password": str(phone)[-6:]}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}
    res = requests.post(url, data=data, headers=headers)
    assert byteify(json.loads(res.text))['status'] == 0
    global_params.token = byteify(json.loads(res.text))['data']['token']
    print "token:" + global_params.token
    print "插入管控后台用户并设置给与权限"
    with db:
        db_cur = db.cursor()
        db_cur.execute(
            "INSERT INTO `clb_user` VALUES  (null, '18616369918', '27345eea93fa977403c9f0e4471638b8', '18616369918', '18616369917@1.com', '组长', '丁守坤管控', '1', null, '0', '2', '0', '0', null, '2016-06-24 14:21:00', '2016-06-24 14:20:53', null, '1', null, '12')")
        print db_cur._last_executed
        op_uid = int(db_cur.lastrowid)
    print '管控用户创建:' + str(op_uid)
