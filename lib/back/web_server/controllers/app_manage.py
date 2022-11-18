from web_server import app
from flask_cors import cross_origin
from flask import request, jsonify, send_file, make_response
from orm.DatabaseModels import TableApp, TableScript
from orm.SqlHelper import SqlHelper
from util.FileHelper import FileHelper
from util.AppHelper import AppHelper
import os


@app.route('/app_list', methods=["GET", "POST"])
@cross_origin()
def app_list():
    apps = SqlHelper.get_entities(TableApp)
    data = []
    for app in apps:
        data.append({
            'id': app.id,
            'package': app.package_name if app.package_name is not None else '',
            'version': app.version if app.version is not None else '',
            'main_activity': app.main_activity if app.main_activity is not None else '',
            'apk': app.apk_path is not None,
            'source': app.source_code_path is not None
        })
    return jsonify({
        'data': data
    })


@app.route('/update_app', methods=["PUT"])
@cross_origin()
def update_app():
    app_id = request.form.get('app_id')
    package_name = request.form.get('package_name')
    version = request.form.get('version')
    main_activity = request.form.get('main_activity')
    apk_file_obj = request.files.get('apk')
    source_code_obj = request.files.get('source_code')

    if apk_file_obj is not None:
        FileHelper.remove_dir(FileHelper.apk_dir(app_id))
        FileHelper.save(FileHelper.apk_dir(app_id), apk_file_obj)
    if source_code_obj is not None:
        FileHelper.remove_dir(FileHelper.source_code_dir(app_id))
        FileHelper.remove_file(FileHelper.source_code_zip_file(app_id))
        FileHelper.save(FileHelper.app_dir(app_id), source_code_obj)
        FileHelper.rename(os.path.join(FileHelper.app_dir(app_id), source_code_obj.filename),
                          FileHelper.source_code_zip_file(app_id))
        FileHelper.unzip(FileHelper.source_code_zip_file(app_id),
                         FileHelper.source_code_dir(app_id))
    # 更新app信息
    SqlHelper.update(TableApp, {'version': version,
                                'main_activity': main_activity,
                                'apk_path': FileHelper.get_apk_file_path(app_id),
                                'source_code_path': FileHelper.source_code_dir(app_id)}, id=app_id)
    app_row = SqlHelper.get_entity(TableApp, id=app_id)
    app_file = FileHelper.app_info_file(app_id)
    # 保存app信息
    with open(app_file, 'w+') as f:
        f.write(f"appId {app_row.id}\n"
                f"package name {app_row.package_name}\n"
                f"mainActivity {app_row.main_activity}\n"
                f"version {app_row.version}\n"
                f"permissions {app_row.permissions}")

    return jsonify({"info": "success"})


@app.route('/app_info', methods=["GET", "POST"])
@cross_origin()
def app_info():
    app_id = request.form.get('app_id')
    app_row = SqlHelper.get_entity(TableApp, id=app_id)
    data = {'id': app_id,
            'package': app_row.package_name,
            'version': app_row.version,
            'main_activity': app_row.main_activity,
            'apk': app_row.apk_path is not None,
            'source': app_row.source_code_path is not None}
    return jsonify({'data': data})


@app.route('/commit_app', methods=["POST"])
@cross_origin()
def commit_app():
    apk_file_obj = request.files.get('apk')
    source_code_obj = request.files.get('source_code')
    temp_id = FileHelper.generate_temp_id()
    apk_file_path = FileHelper.upload_apk(temp_id, apk_file_obj)
    source_code_path = None
    if source_code_obj is not None:
        source_code_path = FileHelper.upload_source_code(temp_id, source_code_obj)
    # 创建app
    AppHelper.create_app(apk_file_path, source_code_path, True, True)
    # 删除临时文件
    FileHelper.remove_dir(FileHelper.temp_file_dir(temp_id))
    return jsonify({"info": "success"})


@app.route('/download_apk', methods=["GET", "POST"])
@cross_origin()
def download_apk():
    app_id = request.form.get('app_id')
    apk_path = FileHelper.get_apk_file_path(app_id)
    apk_name = apk_path.split('/')[-1]
    response = make_response(send_file(apk_path,
                                       mimetype='application/octet-stream',  # 类型检测可以不在这里进行
                                       as_attachment=True,
                                       attachment_filename=apk_name,
                                       ))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response


@app.route('/download_source', methods=["GET", "POST"])
@cross_origin()
def download_source():
    app_id = request.form.get('app_id')
    source_code_zip = FileHelper.source_code_zip_file(app_id)
    response = make_response(send_file(source_code_zip,
                                       mimetype='application/octet-stream',  # 类型检测可以不在这里进行
                                       as_attachment=True,
                                       attachment_filename='project.zip'
                                       ))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response


@app.route('/get_scripts', methods=["GET", "POST"])
@cross_origin()
def get_scripts():
    front = request.get_json(silent=True)
    app_id = int(front["appId"])
    script_rows = SqlHelper.get_entities(TableScript, app_id=app_id)
    data = []
    for row in script_rows:
        data.append(row.id)
    return jsonify({'data': data})
