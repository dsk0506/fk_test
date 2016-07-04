# coding:utf-8
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_apply_type_list():
    log('apply_type', "申请单列表开始")
    data = {"item_type":"19"}
    rs = global_params.post('/apply/type/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('apply_type', "申请单列表成功")







