# -*- coding:UTF-8-*-
import global_params
from common import log


def check_response(response):
    """
    列表结果检测
    :param response:
    :return:
    """
    assert response['status'] == 0, response['message']
    next_start_index = response['data']['next_start_index']
    list_count = len(response['data']['list'])
    if list_count >= 0 and list_count < 15:
        assert int(next_start_index) == -1
    else:
        assert next_start_index == 15
    pass


def send_check(data):
    response = global_params.post('apply/search/list', data)
    check_response(response)
    # 审批进行中
    data['status'] = 3
    check_response(response)
    # 审批已通过
    data['status'] = 1
    check_response(response)
    # 审批被退回
    data['status'] = 2
    check_response(response)
    pass


def test_apply_list():
    """
    申请单列表测试
    :return:
    """
    log('apply', '申请单列表测试开始')
    #全部申请单
    data = {'start_date': '2016-01-01', 'end_date': '2016-07-01', 'item_type': 19, 'status': 0}
    send_check(data)
    log('apply', '申请单列表测试结束')
    pass


def test_expense_list():
    """
    报销单列表测试
    :return:
    """
    log('apply', '报销列表测试开始')
    # 全部申请单
    data = {'start_date': '2016-01-01', 'end_date': '2016-07-01', 'item_type': 20, 'status': 0}
    send_check(data)
    log('apply', '报销单列表测试结束')
    pass


def test_cost_list():
    """
    费用列表测试
    :return:
    """
    log('apply', '费用列表测试开始')
    #全部费用
    data = {'start_date': '2016-06-01', 'end_date': '2016-07-01', 'item_type': 11, 'status': 0}
    response = global_params.post('apply/search/list', data)
    check_response(response)
    #费用已报销
    data['status'] = 1
    response = global_params.post('apply/search/list', data)
    check_response(response)
    #费用未报销
    data['status'] = 3
    response = global_params.post('apply/search/list', data)
    check_response(response)
    log('apply', '费用列表测试结束')
    pass


def test_my_apply_list():
    """
    我的申请单
    :return:
    """
    log('mine', '我的申请单测试开始')
    data = {'agent': 1, 'next_start_index': 0}
    response = global_params.post('apply/requisition/list', data)
    check_response(response)
    log('mine', '我的申请单测试结束')
    pass


def test_my_expense_list():
    """
    我的报销单
    :return:
    """
    log('mine', '我的报销单测试开始')
    data = {'agent': 1, 'next_start_index': 0}
    response = global_params.post('apply/expense/list', data)
    check_response(response)
    log('mine', '我的报销单测试结束')
    pass


def test_my_cost_list():
    """
    费用
    :return:
    """
    log('mine', '我的费用列表测试开始')
    data = {'agent': 1, 'next_start_index': 0}
    response = global_params.post('apply/cost/list', data)
    check_response(response)
    log('mine', '我的费用列表测试结束')
    pass