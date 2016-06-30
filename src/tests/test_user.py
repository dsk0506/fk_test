# coding:utf-8
import global_params
from common import log
import json

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


def test_calendar_checkin_detail():
    log('calendar', "签到详情开始")
    data = {"checkin_id": 1}
    rs = global_params.post('/calendar/checkin/detail', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['content'] == '测试', rs['message']
    log('calendar', "签到详情成功")


def test_calendar_daily_detail():
    log('calendar', "日报详情开始")
    data = {"daily_id": 1}
    rs = global_params.post('/calendar/daily/detail', data)
    assert rs['status'] == 0, rs['message']
    assert rs['data']['content'] == '我的日报', rs['message']
    log('calendar', "日报详情成功")


def test_calendar_checkin_poi():
    log('calendar', "兴趣点开始")
    data = {"keyword": "", "lat": "31.27690836588542", "lng": "121.5386794704861", "next_start_index": 0, "type": 1}
    rs = global_params.post('/calendar/checkin/poi', data)
    assert rs['status'] == 0, rs['message']
    log('calendar', "兴趣点成功")


def test_ucenter_level_create():
    log('ucenter', "职级创建开始")
    data = {"title": "ceo"}
    rs = global_params.post('/ucenter/level/create', data)
    assert rs['status'] == 0, rs['message']
    data = {"title": "总经理"}
    rs = global_params.post('/ucenter/level/create', data)
    assert rs['status'] == 0, rs['message']
    data = {"title": "副总经理"}
    rs = global_params.post('/ucenter/level/create', data)
    assert rs['status'] == 0, rs['message']
    log('ucenter', "职级创建成功")


def test_ucenter_level_list():
    log('ucenter', "职级列表开始")
    data = {}
    rs = global_params.post('/ucenter/level/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 3, rs['message']
    log('ucenter', "职级列表成功")


def test_ucenter_level_delete():
    log('ucenter', "职级删除开始")
    data = {"level_id": "1"}
    rs = global_params.post('/ucenter/level/delete', data)
    assert rs['status'] == 0, rs['message']
    data = {}
    rs = global_params.post('/ucenter/level/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 2, rs['message']
    log('ucenter', "职级删除成功")


def test_ucenter_level_update():
    log('ucenter', "职级更新开始")
    title = "副总经理"
    data = {"level_id": "3", "title": title}
    rs = global_params.post('/ucenter/level/update', data)
    assert rs['status'] == 0, rs['message']
    data = {}
    rs = global_params.post('/ucenter/level/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 2, rs['message']
    assert rs['data']['list'][1]['title'] == title, rs['message']
    log('ucenter', "职级更新成功")


def test_ucenter_level_exchange():
    log('ucenter', "职级排序开始")
    data = {"source_id": "2", "target_id": "3"}
    rs = global_params.post('/ucenter/level/exchange', data)
    assert rs['status'] == 0, rs['message']
    data = {}
    rs = global_params.post('/ucenter/level/list', data)
    assert rs['status'] == 0, rs['message']
    assert len(rs['data']['list']) == 2, rs['message']
    assert rs['data']['list'][1]['title'] == '总经理', rs['message']
    log('ucenter', "职级排序成功")


def test_ucenter_level_cabin(cur):
    log('ucenter', "限制机票舱开始")
    json_string = json.dumps([{"level_id": "2", "title": "总经理", "cabin_rank": "1", "rank": "1"}])
    data = {"cabin_rank": json_string}
    rs = global_params.post('/ucenter/level/cabin', data)
    assert rs['status'] == 0, rs['message']
    cur.execute("select * from clb_user_level where id=2")
    rs = cur.fetchone()
    assert rs[3] == 1
    log('ucenter', "限制机票舱成功")


def test_cost_center_list():
    log('cost_center', "费用中心列表开始")
    data = {"enable": "1"}
    rs = global_params.post('/cost_center/list', data)
    assert rs['status'] == 0, rs['message']
    log('cost_center', "费用中心列表成功")


def test_ucenter_user_invite():
    log('cost_center', "邀请员工开始")
    data = {"fullname": "帅哥", "email": "dsk0506@163.com", "superior": "-1", "cost_center_id": 13, "level_id": 2,
            "telephone": "18616369919"}
    rs = global_params.post('/ucenter/user/invite', data)
    assert rs['status'] == 0, rs['message']
    log('cost_center', "邀请员工成功")


def test_ucenter_user_getcode(cur):
    log('cost_center', "获取激活验证码开始")
    phone = "18616369919"
    data = {"verify_type": 1, "verify_field": phone, "is_check": 1}
    rs = global_params.post('/ucenter/user/getcode', data)
    assert rs['status'] == 0, rs['message']
    cur.execute("select * from clb_verify where field=%(phone)s", {"phone": phone})
    rs = cur.fetchone()
    captcha = rs[4]
    log('cost_center', "获取激活验证码成功")
    data = {"verify_type": 1, "verify_code": captcha, "verify_field": phone, "is_modify": 0}
    rs = global_params.post('/ucenter/user/verify', data)
    hash = rs['data']['hash']
    password = 123456
    data = {"telephone":phone,"password":password,"hash":hash,"superior":-1}
    rs = global_params.post('/ucenter/user/activate', data)
    assert rs['status'] == 0, rs['message']
    data = {'username': phone, "password": password}
    rs = global_params.post('/ucenter/login', data)
    assert rs['status'] == 0
    log('cost_center', "激活用户成功")




