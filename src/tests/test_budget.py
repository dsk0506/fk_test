# -*- coding:UTF-8-*-
from common import db
import global_params


def test_budget_create():
    #获取费用科目
    db_cur = db.cursor()
    db_cur.execute('select id from clb_cost_subject where enable = 1 and company_id = 2')
    result = db_cur.fetchone()
    cost_subject_id = result[0]
    response = global_params.post('budget/subject/title-create', {'subject_id': cost_subject_id})
    assert response['status'] == 0,response['message']
    pass


def test_budget_list():
    response = global_params.post('budget/subject/list')
    assert response['status'] == 0,response['message']
    assert len(response['data']) == 1
    pass


def test_budget_detail():
    db_cur = db.cursor()
    db_cur.execute('select subject_id from clb_budget_subject where company_id = 2')
    result = db_cur.fetchone()
    cost_subject_id = result[0]
    response = global_params.post('budget/subject/detail', {'subject_id': cost_subject_id})
    assert response['status'] == 0,response['message']
    assert len(response['data']['list']) == 1
    pass


def test_budget_particular():
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
    pass

