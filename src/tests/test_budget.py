# coding:utf-8
import requests
import json
import MySQLdb
import global_params
from conftest import cur


def auth(func):
    def real_auth():
        global cur
        cur.execute('select clb_user.* from clb_user,clb_usertoken \
        where clb_usertoken.token=%s and clb_usertoken.user_id = clb_user.id;', (global_params.token))
        user = cur.fetchone()
        if(not user):
            raise LookupError('用户未登录')
        func(user)
    return real_auth

@auth
def standard_create(user):
    data = {'cost_type_id': 10, 'formula': 0, 'list':[{"user_level_id":"20","city_level_id":-1,"money":"300"}]}
    response = global_params.post('cost_center/create', data)
    return response


def test_standard_create():
    data = standard_create()
    assert data['status'] == 0
    return

