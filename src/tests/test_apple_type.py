# coding:utf-8
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_apply_type_list():
    log('apply_type', "申请单类型列表开始")
    data = {"item_type": "19"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('apply_type', "申请单类型列表成功")


def test_apply_type_create():
    log('apply_type', "申请单类型创建开始")
    data = {"item_type": "19", "title": "申请单类型添加测试", "content": "申请单类型添加测试", "cost_able": 1}
    rs = global_params.post('/apply/type/create', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == "申请单类型添加测试", rs['message']
    apply_type = rs['data']['apply_type']
    data = {"item_type": "19"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 4, rs['message']
    log('apply_type', "申请单类型创建成功")
    log('apply_type', "申请单类型修改开始")
    data = {"item_type": "19", "title": "123", "content": "123", "cost_able": 0,"apply_type":apply_type}
    rs = global_params.post('/apply/type/update', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == "123", rs['message']
    log('apply_type', "申请单类型修改成功")
    data = {"apply_type": apply_type}
    rs = global_params.post('/apply/type/delete', data)
    assert rs['status'] == 0, rs['message']
    data = {"item_type": "19"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('apply_type', "申请单类型删除成功")
    log('apply_type', "申请单类型排序开始")
    json_string = json.dumps([{"id": 7, "sort": 0}, {"id": 8, "sort": 1}, {"id": 9, "sort": 2}])
    data = {"sort": json_string}
    rs = global_params.post('/apply/type/sort', data)
    assert rs['status'] == 0, rs['message']
    log('apply_type', "申请单类型排序成功")
