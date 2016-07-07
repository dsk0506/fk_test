# coding:utf-8
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_apply_home_config():
    log('home_config', '获取首页配置开始')
    rs = global_params.post('home/configuration')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页配置成功')


def test_requisition_form(cur):
    log('ucenter_user', "邀请员工开始")
    data = {"fullname": "新用户3", "email": "dsk0333@163.com", "superior": "-1", "cost_center_id": 13, "level_id": 2,
            "telephone": "18616369920"}
    rs = global_params.post('/ucenter/user/invite', data)
    assert rs['status'] == 0, rs['message']
    log('ucenter_user', "邀请员工成功")
    log('ucenter_user', "获取激活验证码开始")
    phone = "18616369920"
    data = {"verify_type": 1, "verify_field": phone, "is_check": 1}
    rs = global_params.post('/ucenter/user/getcode', data)
    assert rs['status'] == 0, rs['message']
    cur.execute("select * from clb_verify where field=%(phone)s", {"phone": phone})
    rs = cur.fetchone()
    captcha = rs[4]
    log('ucenter_user', "获取激活验证码成功")
    data = {"verify_type": 1, "verify_code": captcha, "verify_field": phone, "is_modify": 0}
    rs = global_params.post('/ucenter/user/verify', data)
    hash = rs['data']['hash']
    password = 123123
    data = {"telephone": phone, "password": password, "hash": hash, "superior": -1}
    rs = global_params.post('/ucenter/user/activate', data)
    assert rs['status'] == 0, rs['message']
    data = {'username': phone, "password": password}
    rs = global_params.post('/ucenter/login', data)
    assert rs['status'] == 0
    log('cost_center', "激活用户成功")
    user_id = rs['data']['user_id']
    log('cost_center', '成本中心创建测试开始')
    response = global_params.post('cost_center/list')
    cost_center_data = response['data']
    top_id = cost_center_data['list'][0]['cost_center_id']
    assert top_id != 0
    data = {'pid': top_id, 'serial_no': 'aabbccdd', 'title': '全程费控top2', 'user_id': user_id}
    cost_center = global_params.post('cost_center/create', data)
    assert cost_center['status'] == 0, cost_center['message']
    log('cost_center', '成本中心创建测试结束')
    log('requisition_form', '获取申请单表单开始')
    data = {'apply_type': 7}
    rs = global_params.post('apply/requisition/form', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['custom']) == 4, rs['message']
    log('requisition_create', '创建申请单开始')
    data = {'apply_type': 7, 'cost_center': '{"cost_center_id": 14, "title": "全程费控top2", "serial_no": "aabbccdd"}',
            rs['data']['custom'][0]['key']: '你的时候', rs['data']['custom'][1]['key']: 255,
            rs['data']['custom'][2]['key']: 2, rs['data']['custom'][3]['key']: '是的', 'title': '申请单创建1'}
    rs = global_params.post('apply/requisition/create', data)
    assert rs['status'] == 0, rs['message']
    log('requisition_form', '获取申请单表单结束')
    apply_id = rs['data']['apply_id']
    log('requisition_detail', '获取申请单表单详情开始')
    data = {'apply_id': apply_id}
    rs = global_params.post('apply/requisition/detail', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '我的申请单列表开始')
    rs = global_params.post('apply/requisition/list')
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1
    log('apply_list', '我的申请单列表结束')
    log('approve_withdraw', '撤回申请单开始')
    data = {'action': 11, 'apply_id': apply_id, 'explain': '撤回'}
    rs = global_params.post('approve/update', data)
    assert rs['status'] == 0, rs['message']
    log('requisition_form', '撤回申请单结束')
    log('requisition_form', '编辑申请单开始')
    data = {'apply_id': apply_id, 'apply_type': 7}
    rs = global_params.post('apply/requisition/form', data)
    assert rs['status'] == 0, rs['message']
    log('requisition_form', '编辑申请单结束')
    log('requisition_resubmit', '重新提交申请单开始')
    data = {'apply_type': 7, 'cost_center': '{"cost_center_id": 14, "title": "全程费控top2", "serial_no": "aabbccdd"}',
            rs['data']['custom'][0]['key']: '你的时候', rs['data']['custom'][1]['key']: 255,
            rs['data']['custom'][2]['key']: 2, rs['data']['custom'][3]['key']: '是的', 'title': '重新提交申请单1'}
    rs = global_params.post('apply/requisition/create', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == '重新提交申请单1'
    log('requisition_resubmit', '重新提交申请单结束')

    log('expense_form', '获取报销单表单开始')
    data = {'apply_type': 10}
    rs = global_params.post('apply/expense/form', data)
    assert rs['status'] == 0, rs['message']
    log('expense_form', '获取报销单表单结束')



