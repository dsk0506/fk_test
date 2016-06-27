# coding:utf-8
import requests
import json


def test_login(mongo_cur):
    print  mongo_cur.apply.find_one({'apply_id':4644})
    pass

