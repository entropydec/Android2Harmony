from sqlalchemy import (create_engine, Column, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer, Float, Text, LargeBinary

# from sshtunnel import SSHTunnelForwarder
#
# ssh_host = "210.28.133.13"  # 堡垒机ip地址或主机名
# ssh_port = 20794  # 堡垒机连接mysql服务器的端口号，必须是数字
# ssh_user = "root"  # 这是你在堡垒机上的用户名
# ssh_password = "vmonline@seg"  # 这是你在堡垒机上的用户密码
# mysql_host = "127.0.0.1"  # 这是你mysql服务器的主机名或ip地址
# mysql_port = 3306  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
# mysql_user = "vmplayer"  # 这是你mysql数据库上的用户名
# mysql_password = "VM@online123"  # 这是你mysql数据库的密码
# mysql_db = "vmonline"  # mysql服务器上的数据库名

Base = declarative_base()


class TableUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    pwd = Column(String(100))
    priority = Column(String(100))
    max_buffer_size = Column(Integer, default=314572800)

    def __str__(self):
        return f"id:{self.id},name:{self.name},email:{self.email},pwd:{self.pwd},priority:{self.priority},max_buffer_size:{self.max_buffer_size}"


class TableApp(Base):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(45))
    package_name = Column(String(100))
    version = Column(String(100))
    apk_path = Column(Text)
    source_code_path = Column(Text)
    main_activity = Column(Text)
    permissions = Column(Text)

    def __str__(self):
        return f"package_name:{self.package_name},version:{self.version},id:{self.id},apk_path:{self.apk_path}"


class TableARP(Base):
    __tablename__ = 'arp'
    arp_id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer)
    create_time = Column(String(128))
    update_time = Column(String(128))


class TableTask(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    app_id = Column(Integer)
    arp_id = Column(Integer)
    strategy = Column(String(100))
    parameters = Column(Text)
    status = Column(String(100))
    commit_time = Column(String(100))
    start_time = Column(String(100))
    finished_time = Column(String(100))
    end_time = Column(String(100))


class TableTransition(Base):
    __tablename__ = 'transition'
    id = Column(Integer, primary_key=True)
    arp_id = Column(Integer, primary_key=True)
    # task_id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    target_id = Column(Integer)
    trigger_action = Column(String(100))
    trigger_identifier = Column(Text)
    conditions = Column(Text)


class TableState(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    arp_id = Column(Integer, primary_key=True)
    # task_id = Column(Integer, primary_key=True)
    # package = Column(Text)
    activity = Column(Text)
    picture = Column(String(200))
    layout = Column(String(200))


class TableResult(Base):
    __tablename__ = 'result'
    task_id = Column(Integer, primary_key=True)
    url = Column(String(200))
    instruction_coverage = Column(Float)
    branch_coverage = Column(Float)
    cxty_coverage = Column(Float)
    line_coverage = Column(Float)
    method_coverage = Column(Float)
    class_coverage = Column(Float)
    activity_coverage = Column(Float)


class TableScenario(Base):
    __tablename__ = 'scenario'
    id = Column(Integer, primary_key=True)
    arp_id = Column(Integer, primary_key=True)
    # task_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))
    path = Column(String(100))

    # class TableUpload(Base):
    #     __tablename__ = 'upload'
    #     username = Column(String(100))
    #     app_id = Column(Integer)


class TableScript(Base):
    __tablename__ = 'script'
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer)
    path = Column(String(200))

    def __str__(self):
        return f"id:{self.id},task_id:{self.task_id},name:{self.name},description:{self.description},path:{self.path}"
