# 先写数据库的基本配置
USERNAME = 'root'  # 用户名
PASSWORD = 'mysql'  # 数据库密码
HOST = '127.0.0.1'  # 本地地址
PORT = '3306'  # 端口号
DATABASE = 'demo2_db'  # 数据库名字

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
