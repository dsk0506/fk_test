# -*- coding:UTF-8-*-

import requests
import json
import MySQLdb
import global_params
from common import db,log


def auth(func):
    """
    登录验证
    :param func:
    :return:
    """

    def real_auth():
        db_cur = db.cursor()
        db_cur.execute(
            'select clb_user.* from clb_user,clb_usertoken where clb_usertoken.token=%s and clb_usertoken.user_id = clb_user.id',
            [global_params.token])
        user = db_cur.fetchone()
        if (not user):
            raise LookupError('用户未登录')
        return func(user)

    return real_auth


@auth
def hotel_info(params):
    """
    数据请求
    :param params:
    :return:
    """
    response = global_params.post('home/hotel/info')
    return response


def test_hotel_info():
    """
    预订采购管理-机票整体信息
    :param cur:
    :return:
    """
    log('book_hotel', '开始测试酒店预订信息')
    data = hotel_info()
    assert data['status'] == 0
    log('book_hotel', '酒店预订信息测试结束')
    return


@auth
def hotel_policy_update(params):
    """
    数据请求
    :param params:
    :return:
    """
    data = {"value":"酒店政策公示"}
    response = global_params.post('home/hotel/policy_update',data)
    return response


def test_hotel_policy_update():
    """
    酒店管理-酒店政策
    :return:
    """
    log('book_hotel', '开始测试酒店政策')
    data = hotel_policy_update()
    assert data['status'] == 0
    assert data['data']['value'] == "酒店政策公示"
    log('book_hotel', '酒店政策测试结束')
    return


@auth
def hotel_policy_config(params):
    """
    酒店政策公示状态
    :param params
    :return:
    """
    data = {"enable": 1}
    response = global_params.post('home/hotel/policy_config', data)
    return response


def test_hotel_policy_config():
    """
    测试酒店政策公示状态
    :return:
    """
    log('book_hotel', '开始测试酒店政策公示状态')
    data = hotel_policy_config()
    assert data['status'] == 0
    log('book_hotel', '酒店政策公示状态测试结束')
    return


@auth
def hotel_standard_list(params):
    """
    酒店费用标准
    :param params
    :return:
    """

    response = global_params.post('home/hotel/standard_list')
    return response


def test_hotel_standard_list():
    """
    测试酒店费用标准
    :return:
    """
    log('book_hotel', '开始测试酒店费用标准')
    data = hotel_standard_list()
    assert data['status'] == 0
    log('book_hotel', '酒店费用标准测试结束')
    return


def test_hotel_standard_update():
    data = {"list":[{"user_level_id": 32,"city_level_id": 8, "money":300, "status": 0}]}
    response = global_params.post('home/hotel/standard_update', data)
    return response


@auth
def role_update(params):
    """
    请求api
    :param params:
    :return:
    """
    data = {"role":19, "user_id":"10,11,12"}
    response = global_params.post('ucenter/role/update', data)
    return response


def test_role_update():
    """
    酒店白名单
    :return:
    """
    log("book_hotel", '开始测试酒店白名单')
    data = role_update()
    assert data['status'] == 0
    log("book_hotel", "酒店白名单测试结束")
    return