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
def purchase_manage(params):
    """
    数据请求
    :param params:
    :return:
    """
    response = global_params.post('home/company/purchase')
    return response


def test_purchase_manage():
    """
    预订采购管理-机票整体信息
    :param cur:
    :return:
    """
    log('book_flight', '开始测试预订采购机票管理')
    data = purchase_manage()
    assert data['status'] == 0
    log('book_flight', '预订采购机票管理测试结束')
    return


@auth
def home_company_create(params):
    """
    数据请求
    :param params:
    :return:
    """
    data = {"type":"flight_policy_display","value":1}
    response = global_params.post('home/company/create',data)
    return response


def test_home_company_create():
    """
    预订采购管理-机票政策公示展示
    :return:
    """
    log('book_flight', '开始测试机票管理政策展示状态')
    data = home_company_create()
    assert data['status'] == 0
    assert data['data']['value'] == '1'
    log('book_flight', '机票管理政策展示状态测试结束')
    return

@auth
def role_update(params):
    """
    机票白名单数据更新
    :param params
    :return:
    """
    data = {"role": 18, "user_id": "10,11,12"}
    response = global_params.post('ucenter/role/update', data)
    return response


def test_role_update():
    """
    机票白名单更新测试
    :return:
    """
    log('book_flight', '开始测试机票管理白名单更新')
    data = role_update()
    assert data['status'] == 0
    log('book_flight', '机票管理白名单更新测试结束')
    return
