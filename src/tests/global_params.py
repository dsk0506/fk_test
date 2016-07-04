# -*- coding:UTF-8-*-
import requests
import json
from init import byteify

host = 'http://php.fk.com/'
headers = {'Encryption': 'CLB_NONE', 'Agent': '', 'VersionCode': '', 'Token': ''}
token = '3f0a1bad2de6f5ebc9110c685f4a7144'


def post(route, data=None):
    headers['Token'] = token
    response = requests.post(host + route, data=data, headers=headers)
    return byteify(json.loads(response.text))
