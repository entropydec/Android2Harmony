## 可执行ARP模型(App Running Path Model)

ARP模型是对应用运行过程中的UI跳转关系的建模

ARP模型可以表示为五元组<M,S,S0,T,F>

- M：应用元数据

- S：UI状态集合

- S0：初始UI状态

- T：UI跳转集合

- F：功能场景表示





### 可执行ARP元模型

![image-20220621152911043](/Users/xuhao/SeverProjects/online-android-vm-execution/pics/image-20220621152911043.png)





## ARP核心类



### AppRunningPath类

| 属性        | 类型                  | 描述                                                    |
| ----------- | --------------------- | ------------------------------------------------------- |
| arp_id      | int                   | arp编号                                                 |
| app         | App                   | Arp模型对应app                                          |
| create_time | string                | 创建时间                                                |
| update_time | string                | 修改时间                                                |
| states      | dict\<int,State>      | UI状态集合，集合中每个元素是state id和state组成的键值对 |
| transitions | dict\<int,Transition> | UI跳转集合，集合中每个元素是state id和state组成的键值对 |





### State类

| 属性          | 类型            | 描述                |
| ------------- | --------------- | ------------------- |
| state_id      | int             | state编号           |
| arp_id        | int             | arp编号             |
| package_name  | string          | state对应的package  |
| activity_name | string          | state所属的activity |
| picture       | PIL.Image.Image | state的截图         |
| layout        | string          | state的xml布局结构  |



### Transition类

| 属性          | 类型  | 描述              |
| ------------- | ----- | ----------------- |
| transition_id | int   | transition编号    |
| arp_id        | int   | arp编号           |
| source_id     | int   | 跳转前的state编号 |
| target_id     | int   | 跳转后的state编号 |
| event         | Event | 触发的事件        |







### Event类

| 属性               | 类型                 | 描述           |
| ------------------ | -------------------- | -------------- |
| trigger_action     | string               | 触发事件类型   |
| trigger_identifier | dict\<string,object> | 触发事件的条件 |
| conditions         | dict\<string,objest> | 跳转条件       |







### App类

| 属性             | 类型          | 描述                   |
| ---------------- | ------------- | ---------------------- |
| app_id           | int           | app编号                |
| apk_path         | string        | apk文件路径            |
| source_code_path | string        | 源码文件路径           |
| package_name     | string        | app对应的package       |
| main_activity    | string        | app对应的main activity |
| permissions      | list\<string> | app所需的权限          |







### Task类

| 属性                      | 类型                   | 描述                                                      |
| ------------------------- | ---------------------- | --------------------------------------------------------- |
| task_id                   | int                    | task编号                                                  |
| execution_strategy        | string                 | 探索策略                                                  |
| user_id                   | int                    | 用户编号                                                  |
| state_comparison_strategy | string                 | 场景划分策略                                              |
| arp                       | AppRunningPath         | task对应的arp模型                                         |
| parameters                | dict\<string,object>   | 任务参数                                                  |
| instrumentation           | bool                   | 是否有插桩的源码，若为True会生成覆盖度报告，否则不会      |
| status                    | Enum\<TaskStatus>      | 任务的状态                                                |
| commit_time               | string                 | 任务提交时间                                              |
| start_time                | string                 | 探索开始时间                                              |
| finished_time             | string                 | 探索完成时间                                              |
| end_time                  | string                 | 任务结束时间                                              |
| persistence               | Enum\<PersistenceType> | 持久化策略                                                |
| installed                 | bool                   | apk是否已安装，若为True不会再安装app，否则会。默认为False |
| scenarios                 | list\<Scenario>        | arp对应的场景集合                                         |





### Scenario类

| 属性          | 类型   | 描述         |
| ------------- | ------ | ------------ |
| id            | int    | 场景编号     |
| task_id       | int    | task编号     |
| scenario_name | string | 场景名称     |
| description   | string | 场景描述     |
| path          | string | 场景跳转路径 |





### Result类

| 属性     | 类型                | 描述             |
| -------- | ------------------- | ---------------- |
| task     | Task                | 结果对应的task   |
| url      | string              | 结果文件存储路径 |
| coverage | dict\<string,float> | 覆盖度信息       |





## 数据库



### User表

| 字段            | 类型         | 约束                                 | 描述     |
| --------------- | ------------ | ------------------------------------ | -------- |
| id              | int          | primary_key=True, autoincrement=True | user id  |
| name            | varchar(100) |                                      | 用户名   |
| email           | varchar(100) |                                      | 邮箱     |
| pwd             | varcher(100) |                                      | 密码     |
| priority        | varcher(100) |                                      | 优先级   |
| max_buffer_size | int          | default=314572800                    | 存储空间 |



### App表

| 字段             | 类型         | 约束                                 | 描述               |
| ---------------- | ------------ | ------------------------------------ | ------------------ |
| id               | int          | primary_key=True, autoincrement=True | app id             |
| package_name     | varchar(100) |                                      | app所属的package   |
| version          | varchar(100) |                                      | 版本               |
| apk_path         | text         |                                      | apk文件路径        |
| source_code_path | text         |                                      | 源码文件路径       |
| main_activity    | text         |                                      | app的main activity |
| permissions      | text         |                                      | app的权限          |



### ARP表

| 字段        | 类型         | 约束                                 | 描述     |
| ----------- | ------------ | ------------------------------------ | -------- |
| arp_id      | int          | primary_key=True, autoincrement=True | arp id   |
| app_id      | int          |                                      | app id   |
| create_time | varchar(128) |                                      | 创建时间 |
| update_time | varchar(128) |                                      | 更新时间 |



### Task表

| 字段          | 类型         | 约束                                 | 描述         |
| ------------- | ------------ | ------------------------------------ | ------------ |
| id            | int          | primary_key=True, autoincrement=True | task id      |
| user_id       | int          |                                      | user id      |
| app_id        | int          |                                      | app id       |
| arp_id        | int          |                                      | arp id       |
| strategy      | varchar(100) |                                      | 执行策略     |
| parameters    | text         |                                      | 参数         |
| status        | varchar(100) |                                      | 任务状态     |
| commit_time   | varchar(100) |                                      | 任务提交时间 |
| start_time    | varchar(100) |                                      | 探索开始时间 |
| finished_time | varchar(100) |                                      | 探索结束时间 |
| end_time      | varchar(100) |                                      | 任务结束时间 |



### Transition表

| 字段               | 类型         | 约束                        | 描述           |
| ------------------ | ------------ | --------------------------- | -------------- |
| id                 | int          | primary_key(id,arp_id)=True | transition id  |
| arp_id             | int          | primary_key(id,arp_id)=True | arp id         |
| source_id          | int          |                             | 跳转前state id |
| target_id          | int          |                             | 跳转后state id |
| trigger_action     | varchar(100) |                             | 触发事件类型   |
| trigger_identifier | text         |                             | 触发条件       |
| conditions         | text         |                             | 跳转条件       |



### State表

| 字段     | 类型         | 约束                        | 描述                |
| -------- | ------------ | --------------------------- | ------------------- |
| id       | int          | primary_key(id,arp_id)=True | state id            |
| arp_id   | int          | primary_key(id,arp_id)=True | arp id              |
| activity | text         |                             | state所属的activity |
| picture  | varchar(200) |                             | 图片的路径          |
| layout   | varchar(200) |                             | 布局文件的路径      |





### Result表

| 字段                 | 类型         | 约束             | 描述           |
| -------------------- | ------------ | ---------------- | -------------- |
| task_id              | int          | primary_key=True | task id        |
| url                  | varchar(200) |                  | 结果存储路径   |
| instruction_coverage | float        |                  | 指令覆盖度     |
| branch_coverage      | float        |                  | 分支覆盖度     |
| cxty_coverage        | float        |                  | 圈覆盖度       |
| line_coverage        | float        |                  | 行覆盖度       |
| method_coverage      | float        |                  | 方法覆盖度     |
| class_coverage       | float        |                  | 类覆盖度       |
| activity_coverage    | float        |                  | activity覆盖度 |



### Scenario表

| 字段        | 类型         | 约束                         | 描述                          |
| ----------- | ------------ | ---------------------------- | ----------------------------- |
| id          | int          | primary_key(id, arp_id)=True | scenario id                   |
| arp_id      | int          | primary_key(id, arp_id)=True | arp id                        |
| name        | varchar(100) |                              | 场景名称                      |
| description | varchar(100) |                              | 场景描述                      |
| path        | varchar(100) |                              | 场景条件路径，以0-1-2形式保存 |



### Script表

| 字段   | 类型         | 约束                                 | 描述         |
| ------ | ------------ | ------------------------------------ | ------------ |
| id     | int          | primary_key=True, autoincrement=True | script id    |
| app_id | int          |                                      | app id       |
| path   | varcher(100) |                                      | 脚本文件路径 |





### 磁盘存储结构

| 文件/目录             | 位置                                                    | 描述                                                         |
| --------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| project_dir           | 项目根目录                                              | 项目根目录                                                   |
| storage               | {project_dir}/storage                                   | 文件存储位置                                                 |
| users_dir             | {storage}/users                                         | users目录，用户存储任务结果文件                              |
| arps_dir              | {storage}/arps                                          | arps目录，存储arp相关文件                                    |
| apps_dir              | {storage}/apps                                          | apps目录，存储app相关文件                                    |
| temp_dir              | {storage}/temp                                          | 临时文件                                                     |
| sketches_dir          | {storage}/sketches                                      | 草图目录，存储草图查询相关文件                               |
| app_dir               | {apps_dir}/{**app_id**}                                 | app目录，**app id**对应的app的目录                           |
| app_info_file         | {app_dir}/{app.txt}                                     | **app id**对应的app信息文件                                  |
| apk_dir               | {app_dir}/apk                                           | **app id**对应的app的apk文件                                 |
| source_code_dir       | {app_dir}/source_code                                   | **app id**对应的app源码文件                                  |
| source_code_zip_file  | {app_dir}/source_code.zip                               | **app id**对应的app源码文件压缩包                            |
| manifest_file         | {source_code_dir}/app/src/main/AndroidManifest.xml      | **app id**对应的app源码中的AndroidManifest.xml               |
| app_script_dir        | {app_dir}/scripts                                       | **app id**对应的app脚本目录                                  |
| app_script_file       | {app_script_dir}/testcase_{**script_id**}.py            | **app id**对应的app脚本目录中，**script id**对应的脚本文件   |
| user_dir              | {users_dir}/{**user_id**}                               | **user id**对应的用户目录                                    |
| task_dir              | {users_dir}/{**task_id**}                               | **user id**对应的用户目录下，**task id**对应的任务结果目录   |
| task_info_file        | {task_dir}/task.txt                                     | **task id**对应的任务信息文件                                |
| task_script_dir       | {task_dir}/script                                       | **task id**对应的任务目录下的脚本目录                        |
| coverage_dir          | {result_dir}/coverage                                   | **task id**对应的结果目录下的覆盖度目录                      |
| coverage_output_dir   | {coverage_dir}/output                                   | 覆盖度目录下的覆盖度输出文件目录                             |
| coverage_report_dir   | {coverage_dir}/report                                   | 覆盖度目录下的覆盖度报告文件目录                             |
| coverage_temp_dir     | {coverage_dir}/temp                                     | 覆盖度目录下的覆盖度临时目录                                 |
| log_dir               | {result_dir}/log                                        | **task id**对应的结果目录下的日志目录                        |
| crash_log_file        | {log_dir}/crash_log.txt                                 | 日志目录下的崩溃日志文件                                     |
| coverage_log_file     | {log_dir}/icoverage.log                                 | 日志目录下的覆盖度日志文件                                   |
| result_dir            | {task_dir}/result                                       | **task id**对应的结果目录                                    |
| result_zip_file       | {task_dir}/result_{**task_id**}.zip                     | **task id**对应的task目录下的结果压缩文件                    |
| arp_dir               | {arps_dir}/{**arp_id**}                                 | **arp id**对应的arp目录                                      |
| arp_model_dir         | {arp_dir}/model                                         | arp目录下的模型目录                                          |
| screens_dir           | {arp_dir}/screens                                       | arp模型目录下的UI目录                                        |
| screen_file           | {screens_dir}/{**state_id**}.png                        | UI目录下的**state id**对应的UI截图                           |
| layout_file           | {screens_dir}/{**state_id**}.xml                        | UI目录下的**state id**对应的UI布局文件                       |
| jump_pairs_file       | {arp_model_dir}/jump_pairs.txt                          | arp模型目录下的跳转路径文件                                  |
| activity_info_file    | {arp_model_dir}/activity_info.txt                       | arp模型目录下的UI所属的activity文件                          |
| arp_model_zip         | {arp_dir}/arp_model.zip                                 | arp模型压缩包                                                |
| temp_file_dir         | {temp_dir}/{**temp_id**}                                | **temp id**对应的临时文件目录                                |
| temp_apk_dir          | {temp_file_dir}/apk                                     | **temp id**对应临时文件目录下的apk目录                       |
| temp_script_dir       | {temp_file_dir}/script                                  | **temp id**对应临时文件目录下的脚本目录                      |
| temp_source_code_dir  | temp_file_dir/source_code                               | **temp id**对应临时文件目录下的源码目录                      |
| temp_manifest_file    | {temp_source_code_dir}/app/src/main/AndroidManifest.xml | **temp id**对应临时文件目录下的源码中的AndroidManifest.xml文件 |
| sketch_dir            | {sketches_dir}/{**user_id**}                            | **user id**对应的草图查询目录                                |
| sketch_input_dir      | {sketch_dir}/input                                      | 草图输入目录                                                 |
| sketch_input_image    | {sketch_input_dir}/sketch.jpg                           | 草图文件                                                     |
| sketch_model_dir      | {sketch_dir}/model_color                                | 草图模型着色图目录                                           |
| sketch_output         | {sketch_dir}/output                                     | 草图输出目录                                                 |
| sketch_component_json | {sketch_output}/sketch_component.json                   | 草图中识别到的界面（UI），以及界面中的组件（component）      |
| sketch_jump_json      | {sketch_output}/sketch_jump.json                        | 草图中界面间的跳转关系，包括跳转的起止界面和触发跳转的组件   |
| sketch_ui_json        | {sketch_output}/sketch_ui_info.json                     | 草图中识别出的界面的坐标信息                                 |





### SqlHelper 数据库辅助类

实现了Sql语句的封装以及对数据库的基本操作

| 方法名         | 参数                                                         | 返回值                      | 描述               |
| -------------- | ------------------------------------------------------------ | --------------------------- | ------------------ |
| get_entity     | table_cls: 数据库表Base类, **kwargs:where语句条件            | entity                      | 查询单个记录       |
| get_entities   | table_cls: 数据库表Base类, **kwargs:where语句条件            | list\<entity>               | 批量查询           |
| exists         | table_cls: 数据库表Base类, **kwargs:where语句条件            | 存在返回True，否则返回False | 查询记录否存在     |
| add            | table_cls: 数据库表Base类, **kwargs:insert语句条件           |                             | 新增记录           |
| add_return_key | table_cls: 数据库表Base类, primary_key:主键字段名, **kwargs:insert语句条件 | object:主键字段             | 新增记录并返回主键 |
| add_all        | table_cls: 数据库表Base类, *args:insert语句条件              |                             | 批量新增           |
| delete         | table_cls:数据库表Base类, **kwargs:where语句条件             |                             | 删除记录           |
| update         | table_cls:数据库表Base类, new_fields:要更新的字段组成的键值对集合{字段名:更新值}, **kwargs:where语句条件 |                             | 更新记录           |
| init_db        | override:是否覆盖，默认是False                               |                             | 初始化数据库       |
| create_session |                                                              |                             | 创建会话           |





### 数据库表Base类

用于抽象数据库中的表，记录了表的基本信息

```python
Base = declarative_base()


class TableUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    pwd = Column(String(100))
    priority = Column(String(100))
    max_buffer_size = Column(Integer, default=314572800)

class TableApp(Base):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(100))
    version = Column(String(100))
    apk_path = Column(Text)
    source_code_path = Column(Text)
    main_activity = Column(Text)
    permissions = Column(Text)


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
    source_id = Column(Integer)
    target_id = Column(Integer)
    trigger_action = Column(String(100))
    trigger_identifier = Column(Text)
    conditions = Column(Text)


class TableState(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    arp_id = Column(Integer, primary_key=True)
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



class TableScript(Base):
    __tablename__ = 'script'
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer)
    path = Column(String(200))

```

