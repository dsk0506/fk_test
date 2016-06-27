# coding:utf-8
import global_params
from common import log


def test_calendar_checkin_create():
    log('calendar', "签到开始")
    global_params.headers['Token'] = global_params.token
    data = {'address': '上海市杨浦区周家嘴路3388号', 'city_name': '上海市', 'content': '测试', 'lat': '31.27692952473959',
            'lng': '121.5386952039931', 'photo_id': '', 'type': 1}
    rs = global_params.post('/calendar/checkin/create', data)
    assert rs['status'] == 0
    log('calendar', "签到成功")


def test_calendar_daily_create():
    log('calendar', "日报开始")
    global_params.headers['Token'] = global_params.token
    data = {'content': '我的日报'}
    rs = global_params.post('/calendar/daily/create', data)
    assert rs['status'] == 0
    log('calendar', "日报成功")
