# coding:utf-8
import requests
import json

def test_login():
    print  11
    url = 'http://me.fk2.qa/api/ucenter/login' 
    data = {'username': 'xixi', 'password': '123123'}
    headers = {'Encryption': 'CLB_NONE', 'Agent': '(IOS;1.0.0;IPhone)', 'VersionCode': '5.0.0'}
    res = requests.post(url, data=data, headers=headers)
    user = json.loads(res.text)['data']
    assert res.status_code == 200
    assert user['username'] == 'xixi'

