# coding:utf-8
# 普通审批流测试
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_requisition_approve_list():
    '''
        申请单默认审批流列表
    '''
    params = {'item_type': 19}
    rs = global_params.post('/apply/type/list', params)
    assert rs['status'] == 0
    assert len(rs['data']['list']) == 3
    assert rs['data']['list'][0]['title'] == '采购申请单'


def test_expense_approve_list():
    '''
        报销单默认审批流列表
    '''
    params = {'item_type': 20}
    rs = global_params.post('/apply/type/list', params)
    assert rs['status'] == 0
    assert len(rs['data']['list']) == 3
    assert rs['data']['list'][0]['title'] == '日常报销单'
    

def test_approve_update():
    '''
        更新常规审批流
    '''
    #添加审批人
    approver_params = {'item_type':19, 'type':2, 'nodes':10, 'item_id':7}
    global_params.post('approval/additional/create', approver_params)
    #更新审批流
    node_params = {'item_type': 19, 'item_id': 7, 'node':'[{"node":"1","sort":"1","enable":1},{"node":"2","sort":"2","enable":1},{"node":"3","sort":"3","enable":1},{"node":"4","sort":"4","enable":1},{"node":"5","sort":"5","enable":0}]'}
    global_params.post('approval/workflow-setting/update', node_params)
    #审批流节点长度验证
    list_params = {'item_type': 19, 'item_id': 7}
    rs = global_params.post('approval/workflow-setting/list', list_params)
    available_nodes = [node for node in rs['data']['list'] if node['enable'] == 1]
    assert  len(available_nodes) == 4

