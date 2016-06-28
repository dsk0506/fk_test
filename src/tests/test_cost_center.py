# -*- coding:UTF-8-*-
import global_params
from common import db

def test_cost_center_list():
    """
    成本中心列表，默认创建一个
    :return:
    """
    response = global_params.post('cost_center/list')
    cost_center_data = response['data']
    assert len(cost_center_data['list']) == 1
    assert cost_center_data['total'] == 1
    assert cost_center_data['creatable'] == 0
    return


def test_cost_center_create():
    """
    成本中心创建
    :return:
    """
    response = global_params.post('cost_center/list')
    cost_center_data = response['data']
    top_id = cost_center_data['list'][0]['cost_center_id']
    assert top_id != 0
    data = {'pid': top_id, 'serial_no': 'aabbcc', 'title': '全程费控top'}
    result = global_params.post('cost_center/create', data)
    assert result['status'] == 0
    return


def test_cost_center_update():
    db_cur = db.cursor()
    #取刚创建的cost_center
    db_cur.execute('select * from clb_cost_center order by id desc limit 1')
    cost_center_data = db_cur.fetchone()
    print cost_center_data[0]
    return

test_cost_center_update()

def test_cost_center_freeze():
    return


def test_cost_center_unfreeze():
    return


def test_cost_center_overview():
    return


def test_cost_center_items():
    return