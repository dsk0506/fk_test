# -*- coding:UTF-8-*-
import global_params
from common import db, log


def test_cost_center_list():
    """
    成本中心列表，默认创建一个
    :return:
    """
    log('cost_center', '成本中心列表测试开始')
    response = global_params.post('cost_center/list')
    cost_center_data = response['data']
    assert len(cost_center_data['list']) == 1
    assert cost_center_data['total'] == 3
    # assert cost_center_data['creatable'] == 3, response['message']
    log('cost_center', '成本中心列表测试结束')
    return


def test_cost_center_create():
    """
    成本中心创建
    :return:
    """
    log('cost_center', '成本中心创建测试开始')
    response = global_params.post('cost_center/list')
    cost_center_data = response['data']
    top_id = cost_center_data['list'][0]['cost_center_id']
    assert top_id != 0
    data = {'pid': top_id, 'serial_no': 'aabbcc', 'title': '全程费控top'}
    result = global_params.post('cost_center/create', data)
    assert result['status'] == 0, result['message']
    log('cost_center', '成本中心创建测试结束')
    return


def test_cost_center_update():
    """
    成本中心更新
    :return:
    """
    log('cost_center', '成本中心更新测试开始')
    db_cur = db.cursor()
    # 取刚创建的cost_center
    db_cur.execute('select id,pid,user_id from clb_cost_center order by id desc limit 1')
    cost_center_data = db_cur.fetchone()
    id = cost_center_data[0]
    pid = cost_center_data[1]
    user_id = cost_center_data[2]
    data = {'cost_center_id': id, 'title': '全程费控123', 'serial_no': 'qcfk123', 'pid': pid, 'user_id': user_id}
    response = global_params.post('cost_center/update', data)
    assert response['status'] == 0, response['message']
    assert response['data']['title'] == '全程费控123', response['message']
    log('cost_center', '成本中心更新测试结束')
    return


def test_cost_center_freeze():
    """
    成本中心停用
    :return:
    """
    log('cost_center', '成本中心停用测试开始')
    db_cur = db.cursor()
    # 取刚创建的cost_center
    db_cur.execute('select * from clb_cost_center order by id desc limit 1')
    cost_center_data = db_cur.fetchone()
    id = cost_center_data[0]
    data = {'cost_center_id': id}
    response = global_params.post('cost_center/freeze', data)
    assert response['status'] == 0, response['message']
    log('cost_center', '成本中心停用测试结束')
    return


def test_cost_center_unfreeze():
    """
    成本中心启用
    :return:
    """
    log('cost_center', '成本中心启用测试开始')
    db_cur = db.cursor()
    # 取刚创建的cost_center
    db_cur.execute('select * from clb_cost_center order by id desc limit 1')
    cost_center_data = db_cur.fetchone()
    id = cost_center_data[0]
    data = {'cost_center_id': id}
    response = global_params.post('cost_center/freeze', data)
    assert response['status'] == 0, response['message']
    log('cost_center', '成本中心启用测试结束')
    return


def test_cost_center_overview():
    """
    成本中心月度和年度费用测试
    :return:
    """
    # 全部成本中心月度和年度费用
    log('cost_center', '成本中心月度和年度费用测试开始')
    response = global_params.post('cost_center/overview')
    assert response['status'] == 0

    # 单个成本中心月度和年度费用
    db_cur = db.cursor()
    # 取刚创建的cost_center
    db_cur.execute('select * from clb_cost_center order by id desc limit 1')
    cost_center_data = db_cur.fetchone()
    id = cost_center_data[0]
    data = {'cost_center_id': id}
    response = global_params.post('cost_center/overview', data)
    assert response['status'] == 0
    log('cost_center', '成本中心月度和年度费用测试结束')
    return


def test_cost_center_items():
    """
    成本中心报表费用科目占比上方列表
    :return:
    """
    log('cost_center', '成本中心报表上方列表测试开始')
    response = global_params.post('cost_center/items')
    assert response['status'] == 0, response['message']
    log('cost_center', '成本中心报表上方列表测试结束')
    return


def test_cost_center_secondary():
    """
    成本中心费用占比中列表
    :return:
    """
    log('cost_center', '成本中心费用占比列表测试开始')
    response = global_params.post('cost_center/secondary')
    assert response['status'] == 0, response['message']
    log('cost_center', '成本中心费用占比列表测试结束')
    return


def test_cost_center_recent():
    """
    成本中心费用占比中列表
    :return:
    """
    log('cost_center', '成本中心最近使用测试开始')
    response = global_params.post('cost_center/recent')
    assert response['status'] == 0, response['message']
    log('cost_center', '成本中心最近使用测试结束')

