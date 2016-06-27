# coding:utf-8
from config import config
from common import redis_con, db, log, byteify
import os, requests, time, json
import global_params



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
            'email': '393573645@qq.com', 'shortname': '费控', 'license': ''}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0', 'X-From': 'www'}
    company = requests.post(url, data=data, headers=headers)
    company_id = json.loads(company.text)['data']['company_id']
    assert company_id == 1
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
        op_uid = int(db_cur.lastrowid)
        db_cur.execute('INSERT INTO `clb_role`(`user_id`,`role`, `item_id`,`item_type`) VALUES(%s,%s,%s,%s)',[op_uid,16,company_id,15])

    print '管控用户登录'
    data = {'username': str('18616369918'), "password": str(phone)[-6:]}
    res = requests.post(url, data=data, headers=headers)
    assert byteify(json.loads(res.text))['status'] == 0
    token = byteify(json.loads(res.text))['data']['token']

    print '管控用户开通企业'
    url = config.get_config('app', 'host') + '/ucenter/company/open'
    headers['token'] = token
    data = {'company_id': company_id,'principal':principal,'telephone':phone,'email':'393573645@qq.com','fullname_zh':'全程费控公司','surl':'abc','paying_type':1,\
    'enable_book_flight':2,'hotel_book_status':0,'cost_num':3,'expire_time':'2017-06-23','address':'233','phone':'323','header':'qcfk','license':'',\
    'shortname':'qcfk','fullname_en':'','origin':0,'attachment':'','company_certify':1,'status':0,'certified':0,'manager':'','create_at':'',\
    'domain':'http://img.qccost.com/'}
    res = requests.post(url, data=data, headers=headers)
    assert byteify(json.loads(res.text))['status'] == 0
    print '企业开通成功'
    log('test', "正式用户开始登陆")
    url = config.get_config('app', 'host') + '/ucenter/login'
    data = {'username': str(phone), "password": str(phone)[-6:]}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}
    res = requests.post(url, data=data, headers=headers)
    assert byteify(json.loads(res.text))['status'] == 0
    global_params.token = byteify(json.loads(res.text))['data']['token']
    log('test', "token:" + global_params.token)
    log('test', "正式用户登陆成功")
