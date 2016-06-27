# coding:utf-8
import global_params
from common import log

global_params.headers['Token'] = global_params.token


def test_calendar_checkin_create():
    log('calendar', "签到开始")
    data = {'address': '上海市杨浦区周家嘴路3388号', 'city_name': '上海市', 'content': '测试', 'lat': '31.27692952473959',
            'lng': '121.5386952039931', 'photo_id': '', 'type': 1}
    rs = global_params.post('/calendar/checkin/create', data)
    assert rs['status'] == 0, rs['message']
    log('calendar', "签到成功")


def test_calendar_daily_create():
    log('calendar', "日报开始")
    data = {'content': '我的日报'}
    rs = global_params.post('/calendar/daily/create', data)
    assert rs['status'] == 0, rs['message']
    log('calendar', "日报成功")


def test_calendar_schedule_list():
    log('calendar', "我的日程开始")
    data = {}
    rs = global_params.post('/calendar/schedule/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list'][0]['calendar_list']) == 2, rs['message']
    log('calendar', "我的日报成功")


def test_calendar_checkin_list():
    log('calendar', "我的签到列表开始")
    data = {}
    rs = global_params.post('/calendar/checkin/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 1, rs['message']
    log('calendar', "我的签到列表成功")