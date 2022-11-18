#!/usr/bin/env python3
# _*_ coding: utf-8 _*__ * _
# @Time  : 2020/3/10 11:39
# @Author: ChenZIDu
# @File  : setting.py.py


CORS_HEADERS = 'Content-Type'
UPLOAD_FOLDER = r'./upload'

MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "SE2021online@163.com"
MAIL_PASSWORD = "LKOSXOKCTNVXFMIZ"

# _instance_lock = threading.Lock()
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# os.environ['FLASK_DEBUG'] = '1'


# 调试模式是否开启
DEBUG = True

# session 必须要设置key
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

DIALECT = 'mysql'  # 要用的什么数据库
DRIVER = 'mysqlconnector'  # 连接数据库驱动   官方驱动解决1366问题
USERNAME = 'root'  # 用户名
PASSWORD = 'root'  # 密码
HOST = 'localhost'  # 服务器
PORT = '3306'  # 端口
DATABASE = 'flask'  # 数据库名

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
