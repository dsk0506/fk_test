# coding:utf-8
import requests
import json
import MySQLdb
from config import config
from conf_fixture import cur

url = 'http://xlb.local.fk.com/' 
headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}


def _login():
    data = {'username': '17092123123', 'password': '123123'}
    res = requests.post(url + 'ucenter/login', data=data, headers=headers)
    user = json.loads(res.text)['data']
    return user


def _post(route, data):
    user = _login()
    headers['Token'] = user['token']
    response = requests.post(url + route, data=data, headers=headers)
    return json.loads(response.text)


def _principal(user_id):
    '''
        格式化用户
    '''    
    cur = _connect_mysql()
    cur.execute('select * from clb_user where id = %s' % user_id)
    user = cur.fetchone()
    principal = {
        u'user_id': user[0],
        u'deleted': 0 if user[16] is None else 1,
        u'telephone': unicode(user[3]),
        u'email': unicode(user[4]),
        u'fullname': unicode(user[6]),
        u'cost_center': []
    }
    return principal


def _connect_mysql():
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=name, port=3306, charset='utf8')
    conn.autocommit(True)
    db_cur = conn.cursor()
    return db_cur 


def _init(db_cur):
    #将自己的用户的company_id改掉
    phone = config.get_config('app','phone')
    query = '''update clb_user set company_id = 777 where telephone = %s''' % phone
    db_cur.execute(query)
    #修改该用户公司的配置，添加成本中心数量
    query = '''insert into clb_company_configuration (company_id, type, value) values (777, 'cost_center_num', 99)'''
    db_cur.execute(query) 
    #清理cost_center数据
    query = '''delete from clb_cost_center where company_id != 777''' 
    db_cur.execute(query) 


def test_init_success(cur):
    _init(cur)


def test_create_success(cur):
    user = _login()
    data = {'pid': 0, 'serial_no': 'serial_no_0001', 'title':'the first test cost center', 'type':'1', 'user_id':0}
    response = _post('cost_center/create', data)
    assert response['status'] == 0

    cost_center_id = response['data']['cost_center_id']
    del response['data']['cost_center_id']

    data_json = json.dumps(response['data'])
    assert data_json == '{"enable": 1, "title": "the first test cost center", "serial_no": "serial_no_0001", "pid": "0", "children": [], "principal": []}'
    cur.execute('select * from clb_cost_center where id = %s' % cost_center_id)
    cost_center = cur.fetchone()
    assert cost_center is not None
    

def test_create_error_serialno_existed():
    '''
        重复添加成本中心错误
    '''
    data = {'pid': 0, 'serial_no': 'serial_no_0001', 'title':'the test cost center', 'type':'1', 'user_id':0}
    _post('cost_center/create', data)
    response = _post('cost_center/create', data)
    data_json = json.dumps(response)
    assert data_json == '{"status": "2510", "message": "\u6210\u672c\u4e2d\u5fc3\u7f16\u53f7\u5df2\u88ab\u4f7f\u7528", "data": []}'


def test_create_error_serialno_none():
    '''
        成本中心编号为空
    '''
    data = {'pid': 0, 'serial_no': '', 'title':'the test cost center', 'type':'1', 'user_id':0}
    response = _post('cost_center/create', data)
    data_json = json.dumps(response)
    assert data_json == '{"status": "2511", "message": "\u6210\u672c\u4e2d\u5fc3\u7f16\u53f7\u672a\u8bbe\u7f6e", "data": []}'


def test_list_success(cur):
    user = _login()
    response = _post('cost_center/list', [])   
    cost_center_data = response['data']
    #获取该用户company_id
    cur.execute('select company_id from clb_user where id = %s' % user['user_id'])
    company_id = cur.fetchone()[0]
    #配置成本中心数量
    cur.execute('''select value from clb_company_configuration where company_id = %s and type = 'cost_center_num' ''' % company_id) 
    res = cur.fetchone()
    total_cost_center_num = int(res[0]) if res is not None else 0
    #成本中心列表
    cur.execute('''select * from clb_cost_center where enable = 1 and company_id = %s''' % company_id)
    cost_center_list_db = cur.fetchmany()
    #成本中心已用数量
    cur.execute('''select count(*) from clb_cost_center where company_id = %s''' % company_id)
    used_cost_center_num = int(cur.fetchone()[0])
    #剩余成本中心数量
    rest_cost_center_num = total_cost_center_num - used_cost_center_num + 1
    assert cost_center_data['creatable'] == rest_cost_center_num
    assert cost_center_data['total'] == total_cost_center_num
    #比对成本中心列表
    cost_center_list = []
    for cost_center in cost_center_list_db:
       cost_center_dict = {
            u'cost_center_id' : int(cost_center[0]),
            u'title' : unicode(cost_center[1]),
            u'serial_no' : unicode(cost_center[3]),
            u'principal' : [],
            u'pid' : 0,
            u'enable' : cost_center[6],
            u'children' : []
        }
       cost_center_list.append(cost_center_dict) 
    assert cost_center_list == cost_center_data['list']
    

# def test_update_success(cur):
    # user = _login()
    # cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])
    # res = cur.fetchone()
    # cost_center_id = res[0] if res is not None else 0
    # #build test data
    # data = {
        # 'cost_center_id': cost_center_id,
        # 'enable': 0,
        # 'pid': 0,
        # 'serial_no': 'serial_no_0002',
        # 'title': 'title have been updated',
        # 'user_id': user['user_id'] 
    # }
    # response = _post('cost_center/update', data)
    # assert response['status'] == 0
    # assert response['message'].encode('utf-8') == '更新成功'
    # #build assert data
    # principal = _principal(user['user_id'])
    # assert_data = {
        # u'enable': u'0',
        # u'title': u'title have been updated',
        # u'serial_no': u'serial_no_0002',
        # u'pid': u'0',
        # u'cost_center_id': int(cost_center_id),
        # u'children': [],
        # u'principal': principal
    # }
    # print assert_data
    # print response['data']
    # assert assert_data == response['data']
    

# def test_update_error_cost_center():
    # #build test data
    # data = {
        # 'cost_center_id': 0,
        # 'enable': 1,
        # 'pid': 0,
        # 'serial_no': 'serial_no_0002',
        # 'title': 'title have been updated',
        # 'user_id': 777 
    # }
    # response = _post('cost_center/update', data)
    # assert response['status'] == 2502
    # assert response['message'].encode('utf-8') == '成本中心不存在'


# def test_freeze_success(cur):
    # user = _login()
    # #获取一个cost_center_id
    # cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])
    # res = cur.fetchone()
    # cost_center_id = res[0] if res is not None else 0
    
    # response = _post('cost_center/freeze', {'cost_center_id': cost_center_id})   
    # assert response['status'] == 0
    # assert response['message'].encode('utf-8') == '停用成功'
    # #判断数据在数据库中是否生效 
    # cur.execute('select enable from clb_cost_center where id = %s' % cost_center_id)
    # response = cur.fetchone()
    # assert response[0] == 0 


# def test_personal_success(cur):
    # user = _login()
    # response = _post('cost_center/personal', {'user_id': user['user_id']})
    # assert response['status'] == 0
    # personal_cost_center = response['data']['list'][0]
    # assert personal_cost_center['user_id'] == user['user_id']
    # assert personal_cost_center['title'] == data['title']
    # assert personal_cost_center['serial_no'] == data['serial_no']


# def test_user_success(cur):
    # user = _login()
    # # insert test data into database
    # cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])  
    # cost_center_id = cur.fetchone()[0]
    # cur.execute('update clb_user set cost_center_id = %s where id = %s' % (cost_center_id, user['user_id']) )
    # #test api
    # response = _post('cost_center/user', {'cost_center_id': cost_center_id})
    # assert response['status'] == 0
    # assert response['data']['list'] == [user['user_id']]


# def test_user_error_empty(cur):
    # '''
        # 当cost_center_id不存在的情况
    # '''
    # response = _post('cost_center/user', {'cost_center_id': -1})
    # assert response['status'] == 0
    # assert response['data']['list'] == []
    

# def test_items_success(cur):
    # user = _login()
    # cur.execute('select * from clb_cost_center where company_id = %s' % user['company_id'])  
    # cost_center = cur.fetchone()
    # response = _post('cost_center/items', {'cost_center_id': cost_center[0]})
    # #build test data
    # assert_data = [{
        # u'parent_cost_center_name': u'',
        # u'cost_center_id': int(cost_center[0]),
        # u'title': unicode(cost_center[1])
    # }]
    # assert assert_data == response['data']['list']
      

# def test_secondary_success(cur):
    # #获取一个父节点
    # user = _login()
    # cur.execute('select * from clb_cost_center where enable =1 and company_id = %s' % user['company_id'])  
    # cost_center = cur.fetchone()
    # #向父节点添加一个子节点
    # data = {'pid': cost_center[0], 'serial_no': 'serial_no0003', 'title':'the third test cost center', 'type':'1', 'user_id':7}
    # child_cost_center = _post('cost_center/create', data)['data']
    
    # response = _post('cost_center/secondary',{})
    # assert response['status'] == 0
    # #build assert data
    # assert_data = []
    # assert_data.append({
        # u'parent_cost_center_name': u'',
        # u'cost_center_id': 0,
        # u'cost_center_name': u'\u5168\u516c\u53f8'
    # }) 
    # assert_data.append({
        # u'parent_cost_center_name': unicode(cost_center[1]),
        # u'cost_center_id': int(child_cost_center['cost_center_id']),
        # u'cost_center_name': unicode(child_cost_center['title'])
    # }) 
    # assert assert_data == response['data']['list']


# def test_recent_success(cur):
    # pass


if __name__ == '__main__':
    cur = _connect_mysql()
    test_list_success(cur)
    print('all test passed')
