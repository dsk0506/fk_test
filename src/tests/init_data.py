# -*- coding:UTF-8-*-
from config import config
import global_params


def login(cur,username,password):
    pass


def create_company():
    fullname_zh = config.get_config('company','fullname_zh')
    shortname = config.get_config('company', 'shortname')
    principal = config.get_config('user', 'fullname')
    telephone = config.get_config('user', 'telephone')
    email = config.get_config('company', 'email')
    x_from = global_params.request_header.get('X-From')
    if x_from == 'sales' :
        origin = 1
        certified = 0
        status = 1
    elif x_from == 'operation' :
        origin = 2
        certified = 0
        status = 0
    elif x_from == 'admin' or x_from == 'www' :
        origin = 0
        certified = 0
        status = 1
    else:
        origin = 1
        certified = 0
        status = 0
    pass



def create_user():
    pass