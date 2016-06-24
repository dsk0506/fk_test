# -*- coding:UTF-8-*-
from config import config
from global_params import request_header,app_key
from hashlib import md5
from hashlib import sha1
from conftest import cur

def login(username,password):
    print sha1(password).hexdigest()
    print md5(sha1(password).hexdigest()+app_key).hexdigest()
    print app_key
    mysql_cur = cur()
    mysql_cur.execute('select * from clb_user where username=%s and password=%s',(username,md5(sha1(password).hexdigest()+app_key).hexdigest()))
    user = mysql_cur.fetchone()
    print user
    pass

login('fk005','123123')

def create_company():
    fullname_zh = config.get_config('company','fullname_zh')
    shortname = config.get_config('company', 'shortname')
    principal = config.get_config('user', 'fullname')
    telephone = config.get_config('user', 'telephone')
    email = config.get_config('company', 'email')
    x_from = request_header.get('X-From')
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