from web_server import app
from flask_cors import cross_origin
from flask import request, jsonify
from flask_mail import Message
from threading import Thread
from web_server.common.util import generate_random_str, send_msg, used_size
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableUser


# 1.登录
@app.route('/login', methods=['post'])
@cross_origin()
def login():
    data = request.get_json(silent=True)
    email = data["Email"]
    pwd = data["Password"]
    user_record = SqlHelper.get_entity(TableUser, email=email)
    if user_record is not None and user_record.pwd == pwd:
        id = user_record.id
        name = user_record.name
        priority = user_record.priority
        return jsonify({
            "data": {
                "data": 1,
                "id": id,
                "priority": priority,
                "name": name
            }
        })  # 登陆成功
    else:
        return jsonify({
            "code": 401,
            "message": "unexisted username or wrong password",
            "data": 0
        })  # 用户不存在或密码错误，登录失败


# 2.注册
@app.route('/register', methods=['post'])
@cross_origin()
def registry():
    data = request.get_json(silent=True)
    name = data["UserName"]
    email = data["Email"]
    pwd = data["Password"]
    print(data)
    if SqlHelper.exists(TableUser, name=name, email=email):
        return jsonify({
            "code": 200,
            "message": "register failure",
            "data": 0
        })
    else:  # 该用户名或邮箱已存在,注册失败
        SqlHelper.add(TableUser, name=name, email=email, pwd=pwd, priority=0)
        return jsonify({
            "code": 200,
            "message": "register success",
            "data": 1
        })  # 注册成功


# 3.检验用户名是否已经存在，被登录和注册共用
@app.route('/usernameConfirm', methods=['post'])
@cross_origin()
def confirm_username():
    data = request.get_json(silent=True)
    name = data["UserName"]
    if SqlHelper.exists(TableUser, name=name):
        return jsonify({
            "code": 200,
            "message": "existed username",
            "data": 1
        })  # 该用户名已存在
    else:
        return jsonify({
            "code": 200,
            "message": "unexisted username",
            "data": 0
        })  # 该用户名不存在


@app.route('/storage', methods=['post'])
@cross_origin()
def get_memory():
    front = request.get_json(silent=True)
    username = front["UserName"]
    user_record = SqlHelper.get_entity(TableUser, name=username)
    max_memory = user_record.max_buffer_size
    used_memory = used_size(user_record)
    return jsonify({"MaxMemory": str(max_memory / (1024 * 1024)),
                    "Memory": str(used_memory / (1024 * 1024))})


# 7.修改密码
@app.route('/reset', methods=['post'])
@cross_origin()
def reset_password():
    print("RESET PAWD")
    data = request.get_json(silent=True)
    name = data["UserName"]
    print("name got from front:", name)
    old_pwd = data["OldPassword"]
    new_pwd = data["NewPassword"]
    user_record = SqlHelper.get_entity(TableUser, name=name)
    if user_record.pwd != old_pwd:
        return jsonify({
            "code": 200,
            "message": "wrong old pswd",
            "data": 0
        })  # 原密码错误
    else:
        SqlHelper.update(TableUser, {'pwd': new_pwd}, name=name)
        return jsonify({
            "code": 200,
            "message": "reset password success",
            "data": 1
        })  # 修改密码成功


@app.route("/send_mail", methods=['post'])
@cross_origin()
def send_mail():
    """
    发送邮件
    """
    data = request.get_json(silent=True)
    email = data["Email"]
    message = Message("SE2021online Security code", sender="SE2021online@163.com", recipients=[email])

    random_str = generate_random_str(6)
    message.body = "Please use the following security code for your new account:\n\n\n\n" + random_str + "\n\n\n\nThanks,\nThe SE2021online Team"

    t = Thread(target=send_msg, args=(message,))
    t.start()

    return random_str
