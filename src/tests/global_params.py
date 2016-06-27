# -*- coding:UTF-8-*-
import requests
import json


host = 'http://php.fk.com/'
headers = {'Encryption': 'CLB_NONE', 'Agent': '', 'VersionCode': '', 'Token': ''}
token = ''


def post(route, data=None):
    headers['Token'] = token
    response = requests.post(host + route, data=data, headers=headers)
    return json.loads(response.text)