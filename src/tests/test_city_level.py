# -*- coding:UTF-8-*-
import global_params
from common import log


def city_level_list():
    data = global_params.post('gis/citylevel/list')
    return data


def test_city_level_list():
    """
    城市级别列表
    :return:
    """
    log("city_level", "开始测试城市列表")
    response = city_level_list()
    assert response['status'] == 0
    log("city_level", "城市列表测试结束")
    return


def test_city_type_list():
    """
    城市分类列表
    :return:
    """
    log("city_level", "开始测试城市分类列表")
    response = global_params.post('gis/city/type-list')
    assert response['status'] == 0
    log("city_level", "城市分类列表测试结束")
    return
    return


def test_city_level_create():
    """
    城市级别创建
    :return:
    """
    log("city_level", "开始测试城市级别创建")
    data = {"name":"三线城市","city_ids":"53,62,97"}
    response = global_params.post('gis/citylevel/create', data)
    assert  response['status'] == 0
    log("city_level", "城市级别创建测试结束")
    return


def test_city_level_update():
    """
    城市级别更新
    :return:
    """
    log("city_level", "开始测试城市级别更新")
    data_list = city_level_list()


    level_id = data_list['data'][-1]['id']
    data = {"name": "三线城市", "city_ids": "53,62", "level_id": level_id}
    response = global_params.post('gis/citylevel/update', data)
    assert response['status'] == 0
    log("city_level", "城市级别更新测试结束")
    return

