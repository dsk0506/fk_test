# -*- coding:UTF-8-*-
import global_params
from common import config,db,log
from custom import custom_data


def test_subject_list():
    """
    费用科目列表测试
    :return:
    """
    log('subject', '费用科目列表测试开始')
    data = {'subject': 1, 'with_trashed': 1}
    response = global_params.post('cost_subject/list', data)
    assert response['status'] == 0,response['message']
    #默认创建的3个费用科目
    assert len(response['data']['list']) == 3
    log('subject', '费用科目列表测试结束')
    pass


def test_subject_create():
    """
    费用科目闯创建和删除
    :return:
    """
    log('subject', '费用科目创建测试开始')
    data = {'name': "费用科目测试", 'comment': "test123"}
    response = global_params.post('cost_subject/create', data)
    assert response['status'] == 0,response['message']
    assert response['data']['name'] == "费用科目测试"
    assert response['data']['comment'] == "test123"
    data = {'subject': 1, 'with_trashed': 1}
    response = global_params.post('cost_subject/list', data)
    assert response['status'] == 0, response['message']
    assert len(response['data']['list']) == 4
    log('subject', '费用科目创建测试结束')
    pass


def test_subject_delete():
    """
    费用科目删除
    :return:
    """
    log('subject', '费用科目删除测试开始')
    db_cur = db.cursor()
    db_cur.execute('select id from clb_cost_subject order by id desc limit 1')
    cost_subject_data = db_cur.fetchone()
    subject_id = cost_subject_data[0]

    response = global_params.post('cost_subject/delete', {'subject_id': subject_id})
    assert response['status'] == 0

    data = {'subject': 1, 'with_trashed': 1}
    response = global_params.post('cost_subject/list', data)
    assert response['status'] == 0, response['message']
    assert len(response['data']['list']) == 3

    #还原回去
    db_cur.execute('update clb_cost_subject set enable = 1 where id = %s', [subject_id])
    log('subject', '费用科目删除测试结束')
    pass


def test_subject_add_single_type():
    """
    添加费用类型到费用科目
    :return:
    """
    log('subject', '费用科目添加费用类型测试开始')
    host = config.get_config('app', 'host')
    db_cur = db.cursor()
    db_cur.execute('select id from clb_cost_subject order by id desc limit 1')
    cost_subject_data = db_cur.fetchone()
    subject_id = cost_subject_data[0]
    data = {'title': '测试费用类型', 'surl': '123456', 'icon': 'ad', 'iconPath': host+'/static/assets/cost/ad_2x.png', 'subject_id': subject_id}
    response = global_params.post('cost_type/create', data)
    assert response['status'] == 0, response['message']
    log('subject', '费用科目添加费用类型测试结束')
    pass


def test_cost_type_detail():
    """
    费用类型详情测试
    :return:
    """
    log('subject', '费用类型详情测试开始')
    db_cur = db.cursor()
    db_cur.execute('select clb_cost_type.id from clb_cost_type,clb_cost_subject where clb_cost_type.subject_id = clb_cost_subject.id order by clb_cost_subject.id desc limit 1')
    cost_type_data = db_cur.fetchone()
    type_id = cost_type_data[0]
    data = {'cost_type_id': type_id}
    response = global_params.post('cost_type/detail', data)
    assert response['status'] == 0, response['message']
    assert response['data']['cost_type']['title'] == "测试费用类型"
    assert len(response['data']['custom']) == 12
    log('subject', '费用类型详情测试结束')
    pass


def test_cost_type_deleteAndEnable():
    """
    费用类型停用和启用
    :return:
    """
    log('subject', '费用类型停用和启用测试开始')
    db_cur = db.cursor()
    db_cur.execute(
        'select clb_cost_type.id from clb_cost_type,clb_cost_subject where clb_cost_type.subject_id = clb_cost_subject.id order by clb_cost_subject.id desc limit 1')
    cost_type_data = db_cur.fetchone()
    type_id = cost_type_data[0]
    data = {'cost_type_id': type_id}
    #停用
    response = global_params.post('cost_type/delete', data)
    assert response['status'] == 0,response['message']
    #启用
    response = global_params.post('cost_type/enable', data)
    assert response['status'] == 0, response['message']
    log('subject', '费用类型停用和启用测试结束')
    pass


def test_subject_update():
    """
    费用类型更新
    :return:
    """
    log('subject', '费用类型更新测试开始')
    db_cur = db.cursor()
    db_cur.execute(
        'select clb_cost_type.id from clb_cost_type,clb_cost_subject where clb_cost_type.subject_id = clb_cost_subject.id order by clb_cost_subject.id desc limit 1')
    cost_type_data = db_cur.fetchone()
    type_id = cost_type_data[0]
    data = {'cost_type_id': type_id, 'title': '类型55555', 'surl': '66666', 'icon': 'ad', 'is_days': 0, 'cost_city_enable': 0, 'data': custom_data, 'standards': '{"list":[], "formula": 0}'}
    response = global_params.post('cost_type/total-update', data)
    assert response['status'] == 0,response['message']

    db_cur.execute('select title,surl from clb_cost_type where id = %s',[type_id])
    cost_type = db_cur.fetchone()
    assert cost_type[0] == u'类型55555'
    assert cost_type[1] == '66666'
    log('subject', '费用类型更新测试结束')
    pass

