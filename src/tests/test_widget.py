# coding:utf-8
import global_params
from common import log
import json

global_params.headers['Token'] = global_params.token


def test_default_list():
    '''
        默认自定义项列表
    '''
    rs = global_params.post('/widget/list')
    data = rs['data']
    assert rs['status'] == 0
    assert len(data['list']) == 10
    #简单验证下列表内容
    assert data['list'][0]['title'] == '报销单描述'
    assert data['list'][9]['title'] == '请上传发票照片'


def test_create_input_widget():
    '''
        文本控件创建
    '''
    param = {'data': '''{"title":"文本控件","type":1,"hint":"文本控件","limit":"20"}'''}
    rs = global_params.post('/widget/create', param)
    assert rs['status'] == 0
    assert rs['data']['title'] == '文本控件'
    assert rs['data']['type'] == 1
    

def test_create_money_widget():
    '''
        金额控件创建
    '''
    param = {'data': '''{"title":"金额控件","type":11,"left_maximum":"3","remark":"金额控件","right_maximum":"2"}'''} 
    rs = global_params.post('/widget/create', param)
    assert rs['status'] == 0
    assert rs['data']['title'] == '金额控件'
    assert rs['data']['type'] == 11


def test_delete_widget():
    '''
        删除控件
    '''
    rs = global_params.post('/widget/list')
    data = rs['data']
    assert len(data['list']) == 12

    deleted_data = data['list'][7]
    deleted_data['deleted'] = 1
    param = {'data': json.dumps(deleted_data)} 
    global_params.post('/widget/create', param)

    rs = global_params.post('/widget/list')
    assert len(rs['data']['list']) == 11
    

def test_update_widget():
    '''
        控件更新
    '''
    rs = global_params.post('/widget/list')
    data = rs['data']
    
    #modified data
    modified_data = data['list'][0] 
    modified_data['title'] = '新的控件标题' 
    modified_data['remark'] = '新的控件描述' 
    param = {'data': json.dumps(modified_data)} 
    rs = global_params.post('/widget/create', param)
    assert rs['status'] == 0
    assert rs['data']['title'] == '新的控件标题'
    assert rs['data']['remark'] == '新的控件描述'


def test_define_widget():
    '''
        自定义表单模板的结构列表
    '''
    rs = global_params.post('/widget/defined')
    assert rs['status'] == 0
    assert len(rs['data']) == 21

