# coding:utf-8
import requests
import json
import MySQLdb

url = 'http://me.fk2.qa/api/' 
headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}


def _login():
    data = {'username': 'test', 'password': '123123'}
    res = requests.post(url+'ucenter/login', data=data, headers=headers)
    user = json.loads(res.text)['data']
    return user


def _post(route, data):
    user = _login()
    headers['Token'] = user['token']
    response = requests.post(url+route, data=data, headers=headers)
    return json.loads(response.text)


def test_create_success():
    data = {'pid': 0, 'serial_no': "serial_no0001", 'title':'测试成本中心', 'type':'1', 'user_id':7}
    response = _post('cost_center/create', data)
    assert response['status'] == 0
    del response['data']['cost_center_id']
    data_json = json.dumps(response['data'])
    assert data_json == '{"enable": 1, "title": "\u6d4b\u8bd5\u6210\u672c\u4e2d\u5fc3", "serial_no": "serial_no0001", "pid": "0", "children": [], "principal": []}'


def test_create_error_serialno_existed():
    '''
        重复添加成本中心错误
    '''
    data = {'pid': 0, 'serial_no': "serial_no_existed_0001", 'title':'测试成本中心', 'type':'1', 'user_id':7}
    _post('cost_center/create', data)
    response = _post('cost_center/create', data)
    data_json = json.dumps(response)
    assert data_json == '{"status": "2510", "message": "\u6210\u672c\u4e2d\u5fc3\u7f16\u53f7\u5df2\u88ab\u4f7f\u7528", "data": []}'


def test_create_error_serialno_none():
    '''
        成本中心编号为空
    '''
    data = {'pid': 0, 'serial_no': '', 'title':'测试成本中心', 'type':'1', 'user_id':7}
    response = _post('cost_center/create', data)
    data_json = json.dumps(response)
    assert data_json == '{"status": "2511", "message": "\u6210\u672c\u4e2d\u5fc3\u7f16\u53f7\u672a\u8bbe\u7f6e", "data": []}'


def foo():
    res = cur.execute('select * from clb_user')
    return res

if __name__ == '__main__':
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123123', db='demo27', port=3306)
    cur = conn.cursor()
