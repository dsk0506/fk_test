# -*- coding:UTF-8-*-
import requests
import json


host = 'http://php.fk.com/'
headers = {'Encryption': '', 'Agent': '', 'VersionCode': '', 'Token': ''}
token = ''


def post(route, data):
    headers['Token'] = token
    response = requests.post(host + route, data=data, headers=headers)
    return json.loads(response.text)