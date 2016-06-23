import requests
import json
import global_params

def test_login():
    data = {'username': 'lili', 'password': '123123'}
    res = requests.post(global_params.request_host + 'ucenter/login', data=data, headers=global_params.request_header)
    assert res.status_code == 200
    user = json.loads(res.text)
    assert user['status'] == 0
    return user['data']


def test_daily_create_success(cur):
    user = test_login()
    headers = global_params.request_header
    headers['Token'] = user['token']
    res = requests.post(global_params.request_host + 'calendar/daily/create', data={'content': 'test'}, headers=headers)
    report = json.loads(res.text)['data']

    count = cur.execute('select * from clb_calendar_daily_report where daily_id=?', report['daily_id'])
    assert count == 1