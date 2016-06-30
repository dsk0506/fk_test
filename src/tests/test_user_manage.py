# -*- coding:UTF-8-*-

import global_params
from common import db,config,log

def test_ucenter_user_activate_list(cur):
    log('user_manage', '使用中用户列表测试开始')
    data = {'is_active': 1}
    res = global_params.post('/ucenter/user/list', data)
    assert res['status'] == 0
    assert len(res['data']['list']) == 2
    log('user_manage', '使用中用户列表测试结束')
    pass


def test_ucenter_user_not_activate_list(cur):
    log('user_manage', '已激活未使用用户列表测试开始')
    phone = "18616369919"
    cur.execute('update clb_user set is_active = 2 where telephone = %s' % phone)
    data = {'is_active': 2}
    res = global_params.post('/ucenter/user/list', data)
    assert res['status'] == 0
    print res['data']['list']
    assert len(res['data']['list']) == 1
    log('user_manage', '已激活未使用用户列表测试结束')
    pass


def test_ucenter_user_disabled_list(cur):
    log('user_manage', '已停用用户列表测试开始')
    phone = "18616369919"
    cur.execute('update clb_user set is_active = 0 where telephone = %s' % phone)
    data = {'is_active': 0}
    res = global_params.post('/ucenter/user/list', data)
    assert res['status'] == 0
    assert len(res['data']['list']) == 1
    log('user_manage', '已停用用户列表测试结束')
    pass


def test_ucenter_user_search(cur):
    log('user_manage', '用户搜索测试开始')
    data = {'is_active': 1, 'keyword': '18616369917'}
    res = global_params.post('/ucenter/user/list', data)
    assert res['status'] == 0
    assert res['data']['list'][0]['telephone'] == '18616369917'
    log('user_manage', '用户搜索测试结束')
    pass


def test_user_update():
    log('user_manage', '用户信息更新测试开始')
    phone = config.get_config('app', 'phone')
    db_cur = db.cursor()
    db_cur.execute('select id,fullname,telephone,email,superior,cost_center_id,level_id from clb_user where telephone = %s',[phone])
    user_data = db_cur.fetchone()
    data = {'fullname': '坤123', 'telephone': user_data[2], 'email': user_data[3], 'superior': user_data[4], 'cost_center_id': user_data[5], 'level_id': user_data[6]}

    response = global_params.post('ucenter/user/update', data)

    assert response['status'] == 0,response['message']
    assert response['data']['fullname'] == '坤123',response['message']
    log('user_manage', '用户信息更新测试结束')
    pass


def test_user_role_list():
    log('user_manage', '角色管理测试开始')
    data = {'role': 4}
    response = global_params.post('ucenter/role/list', data)
    assert response['status'] == 0
    log('user_manage', '角色管理测试结束')
    pass


def test_user_role_update():
    log('user_manage', '角色更新测试开始')
    phone = config.get_config('app', 'phone')
    db_cur = db.cursor()
    db_cur.execute('select id from clb_user where telephone = %s',[phone])
    user_data = db_cur.fetchone()
    data = {'role': 4, 'user_id': user_data[0]}
    response = global_params.post('ucenter/role/update', data)
    assert response['status'] == 0
    log('user_manage', '角色更新测试结束')
    pass


def test_user_info_detail():
    log('user_manage', '员工信息维护详情测试开始')
    response = global_params.post('app/configuration/detail', {'item_type': 13})
    assert response['status'] == 0
    log('user_manage', '员工信息维护详情测试结束')


def test_user_info_manage():
    log('user_manage', '员工信息维护测试开始')
    data = {"item_type": 13, "module": '{"superior": "2"}'}
    response = global_params.post('app/configuration/update', data)
    print response
    assert response['status'] == 0,response['message']
    assert response['data']['superior'] == '2'

    data = {'item_type': 13, 'module': '{"superior": 3}'}
    response = global_params.post('app/configuration/update', data)
    assert response['status'] == 0, response['message']
    assert response['data']['superior'] == '3'
    log('user_manage', '员工信息维护测试结束')
