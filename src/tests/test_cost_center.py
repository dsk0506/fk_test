# coding:utf-8
import requests
import json
import MySQLdb

url = 'http://xlb.local.fk.com/' 
headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}


def _login():
    data = {'username': 'test', 'password': '123123'}
    res = requests.post(url + 'ucenter/login', data=data, headers=headers)
    user = json.loads(res.text)['data']
    return user


def _post(route, data):
    user = _login()
    headers['Token'] = user['token']
    response = requests.post(url + route, data=data, headers=headers)
    return json.loads(response.text)
 

def test_create_success(cur):
    data = {'pid': 0, 'serial_no': "serial_no0001", 'title':'the test cost center', 'type':'1', 'user_id':7}
    response = _post('cost_center/create', data)
    assert response['status'] == 0

    cost_center_id = response['data']['cost_center_id']
    del response['data']['cost_center_id']

    data_json = json.dumps(response['data'])
    assert data_json == '{"enable": 1, "title": "the test cost center", "serial_no": "serial_no0001", "pid": "0", "children": [], "principal": []}'
    cur.execute('select * from clb_cost_center where id = %s' % cost_center_id)
    cost_center = cur.fetchone()
    assert cost_center is not None
    

def test_create_error_serialno_existed():
    '''
        重复添加成本中心错误
    '''
    data = {'pid': 0, 'serial_no': "serial_no_existed_0001", 'title':'the test cost center', 'type':'1', 'user_id':7}
    _post('cost_center/create', data)
    response = _post('cost_center/create', data)
    data_json = json.dumps(response)
    assert data_json == '{"status": "2510", "message": "\u6210\u672c\u4e2d\u5fc3\u7f16\u53f7\u5df2\u88ab\u4f7f\u7528", "data": []}'


def test_create_error_serialno_none():
    '''
        成本中心编号为空
    '''
    data = {'pid': 0, 'serial_no': '', 'title':'the test cost center', 'type':'1', 'user_id':7}
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
    cur.execute('''select * from clb_cost_center where company_id = %s''' % company_id)
    cost_center_list_db = cur.fetchmany()
    #成本中心已用数量
    used_cost_center_num = len(cost_center_list_db)
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
    compaire_result = cmp(cost_center_list, cost_center_data['list'])
    assert compaire_result == 0


def test_update_success(cur):
    user = _login()

    cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])
    res = cur.fetchone()
    cost_center_id = res[0] if res is not None else 0
    #build test data
    data = {
        'cost_center_id': cost_center_id,
        'enable': 0,
        'pid': 0,
        'serial_no': 'serial_no_0002',
        'title': 'title have been updated',
        'user_id': user['user_id']
    }
    response = _post('cost_center/update', data)
    assert response['status'] == 0
    assert response['message'].encode('utf-8') == '更新成功'
    #build assert data
    principal = {
        u'user_id': user['user_id'],
        u'deleted': user['deleted'],
        u'telephone': unicode(user['telephone']),
        u'email': unicode(user['email']),
        u'fullname': unicode(user['fullname']),
        u'cost_center': []
    }
    assert_data = {
        u'enable': u'0',
        u'title': u'title have been updated',
        u'serial_no': u'serial_no_0002',
        u'pid': u'0',
        u'cost_center_id': int(cost_center_id),
        u'children': [],
        u'principal': principal
    }

    assert assert_data == response['data']
    

def test_update_error_cost_center():
    #build test data
    data = {
        'cost_center_id': 0,
        'enable': 0,
        'pid': 0,
        'serial_no': 'serial_no_0002',
        'title': 'title have been updated',
        'user_id': 777 
    }
    response = _post('cost_center/update', data)
    assert response['status'] == 2502
    assert response['message'].encode('utf-8') == '成本中心不存在'


def test_freeze_success(cur):
    user = _login()
    #获取一个cost_center_id
    cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])
    res = cur.fetchone()
    cost_center_id = res[0] if res is not None else 0
    
    response = _post('cost_center/freeze', {'cost_center_id': cost_center_id})   
    assert response['status'] == 0
    assert response['message'].encode('utf-8') == '停用成功'
    #判断数据在数据库中是否生效 
    cur.execute('select enable from clb_cost_center where id = %s' % cost_center_id)
    response = cur.fetchone()
    assert response[0] == 0 


def test_unfreeze_success(cur):
    user = _login()
    #获取一个cost_center_id
    cur.execute('select id from clb_cost_center where company_id = %s' % user['company_id'])
    res = cur.fetchone()
    cost_center_id = res[0] if res is not None else 0
    response = _post('cost_center/unfreeze', {'cost_center_id': cost_center_id})   
    print(response)
     


if __name__ == '__main__':
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123123', db='demo27', port=3306)
    cur = conn.cursor()
    test_unfreeze_success(cur)
     
    conn.close()
    print('all test passed')
