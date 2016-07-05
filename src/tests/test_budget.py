# -*- coding:UTF-8-*-
from common import db,log
import global_params


def test_budget_create():
    """
    新建预算
    :return:
    """
    log('budget', '预算创建测试开始')
    #获取费用科目
    db_cur = db.cursor()
    db_cur.execute('select id from clb_cost_subject where enable = 1 and company_id = 2')
    result = db_cur.fetchone()
    cost_subject_id = result[0]
    response = global_params.post('budget/subject/title-create', {'subject_id': cost_subject_id})
    assert response['status'] == 0,response['message']
    log('budget', '预算创建测试结束')
    pass


def test_budget_list():
    """
    预算列表
    :return:
    """
    log('budget', '预算列表测试开始')
    response = global_params.post('budget/subject/list')
    assert response['status'] == 0,response['message']
    assert len(response['data']) == 1
    log('budget', '预算列表测试结束')
    pass


def test_budget_detail():
    """
    预算详情
    :return:
    """
    log('budget', '预算详情测试开始')
    db_cur = db.cursor()
    db_cur.execute('select subject_id from clb_budget_subject where company_id = 2')
    result = db_cur.fetchone()
    cost_subject_id = result[0]
    response = global_params.post('budget/subject/detail', {'subject_id': cost_subject_id})
    assert response['status'] == 0,response['message']
    assert len(response['data']['list']) == 1
    log('budget', '预算详情测试结束')
    pass


def test_budget_particular():
    """
    预算明细
    :return:
    """
    log('budget', '预算明细测试开始')
    db_cur = db.cursor()
    db_cur.execute('select subject_id from clb_budget_subject where company_id = 2')
    result = db_cur.fetchone()
    cost_subject_id = result[0]
    db_cur.execute('select id from clb_cost_center where company_id = 2')
    result = db_cur.fetchone()
    cost_center_id = result[0]
    data = {'subject_id': cost_subject_id, 'cost_center_id': cost_center_id}
    response = global_params.post('budget/subject/particular', data)
    assert response['status'] == 0, response['message']
    assert len(response['data']['list']) == 12
    log('budget', '预算明细测试结束')
    pass

