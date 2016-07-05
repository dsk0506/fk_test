# -*- coding:UTF-8-*-
from common import log
import global_params
import datetime

now = datetime.datetime.now()
data = {'start_date':datetime.datetime(now.year-1,now.month,now.day).strftime('%Y-%m'), 'end_date': now.strftime('%Y-%m'), 'subject_id': 0, 'cost_center_id': 0}


def test_report_overall():
    """
    报表总览
    :return:
    """
    log('report', '报表总览测试开始')
    response = global_params.post('report/company/index')
    assert response['status'] == 0
    log('report', '报表总览测试结束')
    pass


def test_report_cost_detail():
    """
    费用明细
    :return:
    """
    log('report', '报表费用明细测试开始')
    response = global_params.post('report/cost/chart', data)
    assert response['status'] == 0, response['message']
    log('report', '报表费用明细测试结束')
    pass


def test_report_trend():
    """
    费用趋势
    :return:
    """
    log('report', '报表费用趋势测试开始')
    response = global_params.post('report/trend/chart', data)
    assert response['status'] == 0, response['message']
    log('report', '报表费用明细测试结束')
    pass


def test_report_list():
    """
    费用图表源数据
    :return:
    """
    log('report', '报表费用图表测试开始')
    response = global_params.post('report/list', data)
    assert response['status'] == 0, response['message']
    log('report', '报表费用明细测试结束')
    pass


def test_report_costcenter():
    """
    成本中心费用占比
    :return:
    """
    log('report', '报表成本中心费用占比测试开始')
    response = global_params.post('report/cost_center/chart', data)
    assert response['status'] == 0, response['message']
    log('report', '报表成本中心费用占比测试结束')
    pass


def test_report_subject():
    """
    费用科目占比
    :return:
    """
    log('report', '报表费用科目占比测试开始')
    response = global_params.post('report/subject/chart', data)
    assert response['status'] == 0, response['message']
    log('report', '报表费用科目占比测试结束')
    pass
