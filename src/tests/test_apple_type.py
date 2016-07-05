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


def test_expense_type_list():
    log('apply_type', "报销单类型列表开始")
    data = {"item_type": "20"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('apply_type', "报销单类型列表成功")



def test_expense_type_create():
    log('apply_type', "报销单类型创建开始")
    data = {"item_type": "20", "title": "报销单类型添加测试", "content": "报销单类型添加测试"}
    rs = global_params.post('/apply/type/create', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == "报销单类型添加测试", rs['message']
    apply_type = rs['data']['apply_type']
    data = {"item_type": "20"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 4, rs['message']
    log('apply_type', "报销单类型创建成功")
    log('apply_type', "报销单类型修改开始")
    data = {"item_type": "20", "title": "123", "content": "123", "apply_type": apply_type}
    rs = global_params.post('/apply/type/update', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['title'] == "123", rs['message']
    log('apply_type', "报销单类型修改成功")
    widget_data = json.dumps(
        [{"type": 2, "alias": "text", "limit": 20, "key": "title", "title": "报销单名称", "value": "", "required": 1,
          "sort": 11, "remark": "", "hint": "简述相关的事务名称", "replace": "null", "date_format": "null", "detail": 0, "system": 1,
          "deleted": 0, "usage": 1, "display": 1, "visible": 1, "item_id": 13, "item_type": 20, "apply_id": 0,
          "company_id": 2, "updated_at": "2016-07-05 16:19:51"},
         {"type": 4, "alias": "cost_center", "value": [], "key": "cost_center", "title": "成本中心", "required": 1,
          "sort": 12, "remark": "", "hint": "", "replace": "null", "date_format": "null", "detail": 0, "system": 1,
          "deleted": 0, "usage": 1, "display": 1, "visible": 1, "item_id": 13, "item_type": 20, "apply_id": 0,
          "company_id": 2, "updated_at": "2016-07-05 16:19:51"},
         {"key": "relation", "title": "申请单关联", "type": 3, "sort": 10},
         {"type": 2, "alias": "text", "limit": "800", "key": "", "title": "报销单描述", "value": "", "required": "1",
          "sort": 13, "remark": "", "hint": "请填写主管审批所需的详细信息", "replace": "null", "date_format": "null", "detail": 0,
          "system": 0, "deleted": 0, "usage": 1, "display": 1, "visible": 1, "item_id": 0, "item_type": 0,
          "apply_id": 0, "company_id": 2, "updated_at": "2016-01-26 16:23:29", "name": "多行文本控件"},
         {"type": 19, "alias": "photo", "value": [], "key": "", "title": "请上传发票照片", "sort": 14, "remark": "",
          "hint": "", "replace": "null", "date_format": "null", "detail": 0, "system": 0, "deleted": 0, "usage": 1,
          "display": 1, "visible": 1, "item_id": 0, "item_type": 0, "apply_id": 0, "company_id": 2,
          "updated_at": "2016-01-26 15:27:55", "name": "照片控件"}])
    data = {"apply_type": apply_type, "data": widget_data, "printable": 1, "cost_able": 1, "cost_type": 20, "relation_able": 1,
            "related_id": 7}
    rs = global_params.post('/apply/type/update', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['cost_able'] == 1, rs['message']
    assert rs['data']['printable'] == 1, rs['message']
    assert rs['data']['relation_able'] == 1, rs['message']
    assert len(rs['data']['custom']) == 4, rs['message']
    log('apply_type', "报销单配置成功")
    log('apply_type', "报销单类型删除开始")
    data = {"apply_type": apply_type}
    rs = global_params.post('/apply/type/delete', data)
    assert rs['status'] == 0, rs['message']
    data = {"item_type": "20"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('apply_type', "报销单类型删除成功")
    log('apply_type', "报销单类型排序开始")
    json_string = json.dumps([{"id": 11, "sort": 0}, {"id": 12, "sort": 1}, {"id": 10, "sort": 2}])
    data = {"sort": json_string}
    rs = global_params.post('/apply/type/sort', data)
    assert rs['status'] == 0, rs['message']
    data = {"item_type": "20"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['list'][0]['apply_type'] == 11, rs['message']
    log('apply_type', "报销单类型排序成功")