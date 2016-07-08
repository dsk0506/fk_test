# coding:utf-8
# 特殊审批流测试
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_create(cur):
    #创建一个审批用户
    cur.execute('insert into clb_user (id, username, password, fullname, company_id, is_active) values (17, "test_user", "0","测试用户", 2, 1)')
    approver_id = 17

    params = {'user_id': 10, 'content': approver_id, 'item_id': '7,8,9,10,11,12'}
    rs =  global_params.post('/approval/special/create', params) 
    assert rs['status'] == 0
    #检测审批流
    rs = global_params.post('/approval/special/list')
    assert rs['status'] == 0
    assert rs['data']['total'] == 1
    

def test_update():
    params = {'user_id': 10, 'content': 17, 'item_id': '7,8,9', 'ori_id': '7,8,9,10,11,12'}
    rs =  global_params.post('/approval/special/create', params) 
    assert rs['status'] == 0
    rs = global_params.post('/approval/special/list')
    assert len(rs['data']['list'][0]['item']) == 3


def test_delete():
    params = {'user_id': 10, 'item_id': '7,8,9'}
    rs =  global_params.post('/approval/special/delete', params) 
    assert rs['status'] == 0
    rs = global_params.post('/approval/special/list')
    assert rs['status'] == 0
    assert rs['data']['total'] == 0
    


if __name__ == '__main__':
    import MySQLdb
    conn = MySQLdb.connect(host='php.fk.com', user='root', passwd='', db='demo27', port=3306, charset='utf8')
    conn.autocommit(True)
    cur = conn.cursor()
    global_params.token = 'a7d006a7ae524c6528678616b4d284a8'
    test_update() 
    print 'all passed'
