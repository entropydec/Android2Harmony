import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from web_server import app
from web_server.controllers import result_manage, task_manage, user_manage, app_manage, apprepo_manage

if __name__ == '__main__':
    app.run(host='localhost', port=9002, debug=False)
