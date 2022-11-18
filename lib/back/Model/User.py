import os
import shutil
from os.path import join, getsize
import threading

from sqlalchemy.orm import Session

from Model import Task


class User:
    # Finish FIXME: support multithreading
    User_List = {}
    user_list_lock = threading.Lock()
    default_max_buffer_size = 314572800  # 300MB
    # default_max_buffer_size = 20971520 #20MB
    result_folder_abs_addr = "/Users/xuhao/PycharmProjects/SE_project/vm_module-core"

    def __init__(self, name: str, email: str, password: str, priority: str, max_buffer_size: int = None):
        self.name = name
        self.email = email
        self.password = password
        self.priority = priority
        if max_buffer_size:
            self.max_buffer_size = User.default_max_buffer_size

    # 根据名字获取user，若存在则返回一个user对象，否则返回none
    @staticmethod
    def get_user(**kw):
        if 'name' in kw:
            name = kw['name']
            User.user_list_lock.acquire()
            if name in User.User_List:
                item = User.User_List[name]
                User.user_list_lock.release()
                return item
            else:
                session: Session = DBM.MysqlSession()
                item = session.query(DB_User).filter(
                    DB_User.u_name == name).all()
                session.close()
                if len(item) != 0:
                    item = User(
                        item[0].u_name, item[0].u_email, item[0].u_pswd, item[0].u_priority)
                    User.User_List[name] = item
                    User.user_list_lock.release()
                    return item
                else:
                    User.user_list_lock.release()
                    return None
        elif 'email' in kw:
            email = kw['email']
            User.user_list_lock.acquire()
            session: Session = DBM.MysqlSession()
            item = session.query(DB_User).filter(
                DB_User.u_email == email).all()
            session.close()
            if len(item) != 0:
                name = item[0].u_name
                if name in User.User_List:
                    item = User.User_List[name]
                    User.user_list_lock.release()
                    return item
                else:
                    User.User_List[name] = User(
                        name, email, item[0].u_pswd, item[0].u_priority)
                    User.user_list_lock.release()
                return User.User_List[name]
            else:
                User.user_list_lock.release()
                return None

    # 添加一个user
    @staticmethod
    def add_user(name: str, email: str, pswd: str, priority: str):
        session: Session = DBM.MysqlSession()
        item = DB_User(u_name=name, u_email=email,
                       u_pswd=pswd, u_priority=priority, u_max_buffer_size=User.default_max_buffer_size)
        session.add(item)
        session.commit()
        session.close()
        # print('add user: ', str(item))
        item = User(name, email, pswd, priority)
        with User.user_list_lock:
            User.User_List[name] = item
        return item

    # 删除一个user
    @staticmethod
    def del_user(name: str):
        with User.user_list_lock:
            if name in User.User_List:
                User.User_List.pop(name)
        session: Session = DBM.MysqlSession()
        item = session.query(DB_User).filter(DB_User.u_name == name).delete()
        session.commit()
        session.close()

    def used_size(self):
        username = self.name
        max_size = self.max_buffer_size
        # userfold = os.path.join(os.path.abspath('./result'), username)
        RESULT_FOLDER = 'result'
        USER_FOLDER = username
        cur_result_folder_abs_addr = os.path.join(self.result_folder_abs_addr, RESULT_FOLDER)
        userfold = os.path.join(cur_result_folder_abs_addr, USER_FOLDER)
        print("in used_size,userfold:", userfold)
        if not os.path.exists(userfold):
            print("this user haven't got his folder")
            return 0
        used_size = 0
        for root, dirs, files in os.walk(userfold, topdown=False):
            used_size += sum([getsize(join(root, name)) for name in files])
        if used_size < max_size:
            return used_size
        else:
            return max_size

    def get_max_size(self):
        return self.max_buffer_size

    def clear_buffer(self):
        """
        Return: 如果用户文件夹大小比分配的最大存储空间大，则随机删除其中的1/2，返回True; 否则不修改，返回False

        """
        # 获取用户文件夹userfold内的所有文件的当前大小总和used_size(不包括子目录)
        username = self.name
        max_size = self.max_buffer_size
        userfold = os.path.join(os.path.abspath('./result'), username)
        used_size = 0
        for root, dirs, files in os.walk(userfold, topdown=False):
            used_size += sum([getsize(join(root, name)) for name in files])
        if used_size < max_size:
            return False
        else:
            # 删除结束时间最早的一半任务文件夹
            sorted_dirs = sorted(
                dirs, key=lambda x: os.path.getmtime(os.path.join(root, x))
            )
            remove_len = int(len(sorted_dirs) / 2)
            for d in sorted_dirs[:remove_len]:
                Task.del_task(task_id=d)
                shutil.rmtree(os.path.join(root, d))
            return True

    # 把用户和app的上传关系存到upload表里

    def save_to_Upload(self, app_id: str):
        session: Session = DBM.MysqlSession()
        item = DB_Upload(u_username=self._get_name(), u_appid=app_id)
        session.add(item)
        session.commit()
        session.close()
        return item

    def _get_name(self):
        return self.__name

    def _get_email(self):
        return self.__email

    def _get_pswd(self):
        return self.__pswd

    def _get_priority(self):
        return self.__priority

    def _get_max_buffer_size(self):
        return self.__max_buffer_size

    def _set_name(self, name):
        session: Session = DBM.MysqlSession()
        item = session.query(DB_User).filter(DB_User.u_name == name).all()
        old_name = self.__name
        with self.user_list_lock:
            if name in User.User_List or len(item) != 0:
                print("This username has been used")
                return
            User.User_List[name] = User.User_List[old_name]
            User.User_List.pop(old_name)
        self.__name = name
        item = session.query(DB_User).filter(
            DB_User.u_name == old_name).update({DB_User.u_name: name})
        session.commit()
        session.close()
        print('change user name ', old_name, ' to ', name)

    def _set_email(self, email):
        if User.get_user(email=email) is None:
            self.__email = email
            print('change email for user:', email)

    def _set_pswd(self, pswd):
        session: Session = DBM.MysqlSession()
        item = session.query(DB_User).filter(
            DB_User.u_name == self.__name).update({DB_User.u_pswd: pswd})
        session.commit()
        session.close()
        self.__pswd = pswd
        print('change pswd for user:', self.name)

    def _set_max_buffer_size(self, newsize):
        session: Session = DBM.MysqlSession()
        item = session.query(DB_User).filter(DB_User.u_name == self.__name).update(
            {DB_User.u_max_buffer_size: newsize})
        session.commit()
        session.close()
        self.__max_buffer_size = newsize
        print('change buffer size for user:', self.name)

    def _set_priority(self, priority):
        session: Session = DBM.MysqlSession()
        item = session.query(DB_User).filter(
            DB_User.u_name == self.__name).update(
            {DB_User.u_priority: priority})
        session.commit()
        session.close()
        self.__priority = priority
        print('change priority for user:', self.name)

    name = property(_get_name, _set_name)
    email = property(_get_email, _set_email)
    pswd = property(_get_pswd, _set_pswd)
    priority = property(_get_priority, _set_priority)
    max_buffer_size = property(_get_max_buffer_size, _set_max_buffer_size)
