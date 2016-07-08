# coding:utf-8
import global_params
from common import log

global_params.headers['Token'] = global_params.token


def test_apply_home_config():
    log('home_config', '获取首页配置开始')
    rs = global_params.post('home/configuration')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页配置成功')

    log('home_config', '获取首页待办事项开始')
    rs = global_params.post('home/backlog')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页待办事项成功')

    log('home_config', '获取首页我的管理开始')
    rs = global_params.post('home/manage')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页我的管理成功')

    log('home_config', '获取首页我的动态开始')
    rs = global_params.post('home/feed')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页我的动态成功')

    log('home_config', '获取我的个人信息开始')
    rs = global_params.post('ucenter/user/profile')
    assert rs['status'] == 0, rs['message']
    log('home_config', '获取首页我的动态成功')


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
    log('requisition_form', '创建申请单结束')
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
    data = {'apply_id': apply_id, 'apply_type': 7, 'cost_center': '{"cost_center_id": 14, "title": "全程费控top2", "serial_no": "aabbccdd"}',
            rs['data']['custom'][0]['key']: '你的时候', rs['data']['custom'][1]['key']: 255,
            rs['data']['custom'][2]['key']: 2, rs['data']['custom'][3]['key']: '是的', 'title': '重新提交申请单1'}
    rs = global_params.post('apply/requisition/create', data)
    assert rs['status'] == 0, rs['message']
    log('requisition_resubmit', '重新提交申请单结束')

    '''
        更新常规审批流
    '''
    # 添加审批人
    approver_params = {'item_type': 20, 'type': 1, 'nodes': 10, 'item_id': 10}
    global_params.post('approval/additional/create', approver_params)
    # 更新审批流
    node_params = {'item_type': 20, 'item_id': 10,
                   'node': '[{"node":"1","sort":"1","enable":1},{"node":"2","sort":"2","enable":1},{"node":"3","sort":"3","enable":1},{"node":"4","sort":"4","enable":0},{"node":"5","sort":"5","enable":1}]'}
    global_params.post('approval/workflow-setting/update', node_params)
    log('expense_form', '获取报销单表单开始')
    data = {'apply_type': 10}
    rs = global_params.post('apply/expense/form', data)
    assert rs['status'] == 0, rs['message']
    log('expense_form', '获取报销单表单结束')
    log('expense_create', '创建报销单开始')
    data = {'apply_type': 10, 'cost_center': '{"cost_center_id": 14, "title": "全程费控top2", "serial_no": "aabbccdd"}',
            rs['data']['custom'][0]['key']: '自定义文本', 'title': '报销单创建1'}
    rs = global_params.post('apply/expense/create', data)
    assert rs['status'] == 0, rs['message']
    log('requisition_form', '创建报销单结束')
    expense_id = rs['data']['apply_id']
    log('expense_detail', '获取报销单详情开始')
    data = {'apply_id': expense_id}
    rs = global_params.post('apply/expense/detail', data)
    assert rs['status'] == 0, rs['message']
    rs = global_params.post('apply/expense/h5-detail', data)
    assert rs['status'] == 0, rs['message']
    rs = global_params.post('apply/expense/web-detail', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '我的报销单列表开始')
    rs = global_params.post('apply/expense/list')
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1
    log('apply_list', '我的报销单列表结束')

    log('apply_list', '费用类型列表开始')
    data = {'subject': 1, 'form': 1}
    rs = global_params.post('cost/type', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '费用类型列表结束')
    log('apply_list', '费用标准超标开始')
    data = {'city_id': -1, 'cost_type_id': 18}
    rs = global_params.post('budget/standards/cost', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '费用标准超标结束')

    log('apply_list', '费用创建开始')
    data = {'apply_type': 18, 'content': '费用', 'date': '{"start_date":"2016-07-08"}', 'money': 100,
            'related_id': expense_id, 'photo': '[]'}
    rs = global_params.post('apply/cost/create', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '费用创建结束')

    log('expense_report', '费用报表查看开始')
    data = {'apply_id': expense_id}
    rs = global_params.post('apply/expense/report', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '费用报表查看结束')

    log('expense_submit', '提交报销单开始')
    data = {'action': 1, 'apply_id': expense_id}
    rs = global_params.post('approve/update', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '提交报销单结束')

    log('expense_submit', '撤回报销单开始')
    data = {'action': 11, 'apply_id': expense_id, 'explain': '撤回'}
    rs = global_params.post('approve/update', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '撤回报销单结束')

    log('expense_submit', '重新提交报销单开始')
    data = {'action': 4, 'apply_id': expense_id}
    rs = global_params.post('approve/update', data)
    assert rs['status'] == 0, rs['message']
    log('apply_list', '重新报销单结束')

    # '切换用户到审批人'
    data = {"username": 18616369920, "password": 123123}
    rs = global_params.post('/ucenter/login', data)
    assert rs['status'] == 0
    global_params.token = rs['data']['token']
    log('approve_list', '我的待审批申请单列表开始')
    data = {'check_type': 0}
    rs = global_params.post('approval/requisition/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1, rs['message']
    log('approve_list', '我的待审批申请单列表结束')
    log('approve_list', '我的待审批报销单列表开始')
    data = {'check_type': 0}
    rs = global_params.post('approval/expense/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1, rs['message']
    log('approve_list', '我的待审批报销单列表结束')

    log('approve_list', '审批同意申请单开始')
    data = {'action': 2, 'apply_id': apply_id}
    rs = global_params.post('approve/update', data)
    assert rs['status'] == 0, rs['message']
    data = {'check_type': 1}
    rs = global_params.post('approval/requisition/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1, rs['message']
    log('approve_list', '审批同意申请单成功')

    log('approve_list', '批量审批同意报销单开始')
    data = {'action': 2, 'apply_id': expense_id, 'item_type': 20}
    rs = global_params.post('approve/batchapprove', data)
    assert rs['status'] == 0, rs['message']
    data = {'check_type': 1}
    rs = global_params.post('approval/expense/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1, rs['message']
    log('approve_list', '批量审批同意报销单成功')

    # '切换回用户到提交人'
    data = {"username": 18616369917, "password": 123123}
    rs = global_params.post('/ucenter/login', data)
    assert rs['status'] == 0
    global_params.token = rs['data']['token']