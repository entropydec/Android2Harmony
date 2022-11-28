# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from orm.SqlHelper import SqlHelper
import os

app = Flask(__name__)

# 配置部分
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = r'./upload'

app.config["MAIL_SERVER"] = "smtp.163.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "SE2021online@163.com"
app.config["MAIL_PASSWORD"] = "LKOSXOKCTNVXFMIZ"

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['FLASK_DEBUG'] = '1'

CORS(app)

# 实例化flask_mail
mail = Mail()
mail.init_app(app)

# 加载配置文件
# app.config.from_object('web_server.setting')
# app.config.from_envvar('FLASKR_SETTINGS')

# 初始化数据库
SqlHelper.init_db()
