# coding:utf-8
import requests
import json
from conftest import mongo_cur

def test_user():
    assert 1 == 1


def test_mongo(mongo_cur):
    '''
    mongo connect test
    :param mongo_cur:
    :return:
    '''
    print mongo_cur.apply.find_one({'apply_id': 63926})
    return