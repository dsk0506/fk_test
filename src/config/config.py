# encoding:utf-8

import ConfigParser
import os


# 获取config配置文件
def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.conf'
    config.read(path)
    return config.get(section, key)

    # 其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
