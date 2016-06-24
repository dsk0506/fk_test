# coding:utf-8
import requests
import json
import MySQLdb
import global_params
from conftest import cur


def auth(func):
    '''
    登录验证
    :param func:
    :return:
    '''
    def real_auth(cur):
        cur.execute('select clb_user.* from clb_user,clb_usertoken where clb_usertoken.token=%s and clb_usertoken.user_id = clb_user.id',[global_params.token])
        user = cur.fetchone()
        if(not user):
            raise LookupError('用户未登录')
        return func(user)
    return real_auth


@auth
def standard_create(cur):
    '''
    数据请求
    :param cur:
    :return:
    '''
    data = {'cost_type_id': 10, 'formula': 0, 'list':[{"user_level_id":"20","city_level_id":-1,"money":"300"}]}
    response = global_params.post('budget/standards/create', data)
    return response


def test_standard_create(cur):
    '''
    费用标准创建
    :param cur:
    :return:
    '''
    data = standard_create(cur)
    assert data['status'] == 0
    return


@auth
def standard_update(cur):
    '''
    请求数据
    :param cur:
    :return:
    '''
    data = {'cost_type_id': 10, 'formula': 0, 'list': [{"user_level_id": "20", "city_level_id": -1, "money": "300"}]}
    response = global_params.post('budget/standards/update', data)
    return response

def test_standard_update(cur):
    '''
    费用标准更新
    :param cur:
    :return:
    '''
    data = standard_update(cur)
    assert data['status'] == 0
    return