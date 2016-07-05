# -*- coding:UTF-8-*-
import global_params
from common import log


def test_company_update():
    log('ucenter_company', '企业信息维护测试开始')
    #公司名称更新
    fullname_zh = '全程费控111'
    response = global_params.post('ucenter/company/update', {'fullname_zh': fullname_zh})
    assert response['status'] == 0,response['message']
    assert response['data']['fullname_zh'] == fullname_zh, response['message']
    #公司地址更新
    address = '上海市隆昌路'
    response = global_params.post('ucenter/company/update', {'address': address})
    assert response['status'] == 0, response['message']
    assert response['data']['address'] == address, response['message']
    # 公司座机号更新
    phone = '13899999999'
    response = global_params.post('ucenter/company/update', {'phone': phone})
    assert response['status'] == 0, response['message']
    assert response['data']['phone'] == phone, response['message']
    log('ucenter_company', '企业信息维护测试结束')
    pass
