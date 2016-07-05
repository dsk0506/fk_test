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
    data = {"item_type": "19", "title": "123", "content": "123", "cost_able": 0, "apply_type": apply_type}
    rs = global_params.post('/apply/type/update', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == "123", rs['message']
    json_string = json.dumps(
        [{"type": 2, "alias": "text", "limit": 20, "key": "title", "title": "申请事由", "value": "", "required": 1,
          "sort": 10, "remark": "", "hint": "简述您的申请事由", "replace": "null", "date_format": "null", "detail": 1, "system": 1,
          "deleted": 0, "usage": 1, "display": 1, "visible": 1, "item_id": 14, "item_type": 19, "apply_id": 0,
          "company_id": 2, "updated_at": "2016-07-05 09:28:43"},
         {"type": 4, "alias": "cost_center", "value": [], "key": "cost_center", "title": "成本中心", "required": 1,
          "sort": 20, "remark": "", "hint": "", "replace": "null", "date_format": "null", "detail": 0, "system": 1,
          "deleted": 0, "usage": 1, "display": 1, "visible": 1, "item_id": 14, "item_type": 19, "apply_id": 0,
          "company_id": 2, "updated_at": "2016-07-05 09:28:43"}])
    log('apply_type', "申请单类型修改成功")
    data = {"apply_type": apply_type, "data": json_string, "loanable": 0, "printable": 0, "relation_able": 0,
            "budget_type": ""}
    rs = global_params.post('/apply/type/update', data)
    assert rs['status'] == 0, rs['message']
    log('apply_type', "申请单配置成功")
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
