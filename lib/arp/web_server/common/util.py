from os.path import getsize, join

from web_server import app, mail
import os
import random
from util.FileHelper import FileHelper


def send_msg(msg):
    with app.app_context():
        mail.send(msg)


def generate_random_str(random_length=6):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


def used_size(user):
    user_id = user.id
    user_path = FileHelper.user_dir(user_id)
    file_size = FileHelper.get_file_size(user_path)
    return min(file_size, user.max_buffer_size)
