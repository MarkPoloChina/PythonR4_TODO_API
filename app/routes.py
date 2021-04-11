# CPR MP FOR W2OL-PY-R4 2021 A.R.R.
from flask import flash, redirect, url_for, request, jsonify, abort
from app import app, db, token, redis
from sqlalchemy import and_
from app.models import *

#跨域
@app.after_request
def cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

@app.route('/todolist/test')
def test():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    return jsonify({'status': 200, 'message': 'test Ok - CPR MP 2021', 'currentId': currentId})

# 增
@app.route('/todolist/task/add', methods=['POST'])
def add():
    if not request.json or not 'title' in request.json:
        abort(400)
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    newTask = Task(userId=currentId,title=request.json['title'],isDone=False,ddl=datetime(request.json['ddl']['y'],
        request.json['ddl']['m'],request.json['ddl']['d'],request.json['ddl']['h'],request.json['ddl']['min'],request.json['ddl']['s']))
    db.session.add(newTask)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 查 所有事项
@app.route('/todolist/task/get/all', methods=['GET'])
def getAll():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter_by(userId=currentId).all()
    listToOutput = [{"id":task.id, "title":task.title, "time":task.timestamp, "isDone":task.isDone} for task in tasks]
    return jsonify({'status': 200, 'message': 'Ok', 'data': listToOutput})

# 查 关键字
@app.route('/todolist/task/get/keyWord', methods=['GET'])
def search():
    if not request.json or not 'keyWord' in request.json:
        abort(400)
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = db.session.query(Task).filter(and_(Task.title.like('%'+request.json['keyWord']+'%'),Task.userId==currentId)).all()
    listToOutput = [{"id":task.id, "title":task.title, "time":task.timestamp, "isDone":task.isDone} for task in tasks]
    redis.saveHistory(currentId, request.json['keyWord'])
    return jsonify({'status': 200, 'message': 'Ok', 'data': listToOutput})

# 查 已完成事项
@app.route('/todolist/task/get/fin', methods=['GET'])
def getFin():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==True)).all()
    listToOutput = [{"id":task.id, "title":task.title, "time":task.timestamp, "isDone":task.isDone} for task in tasks]
    return jsonify({'status': 200, 'message': 'Ok', 'data': listToOutput})

# 查 未完成事项
@app.route('/todolist/task/get/unFin', methods=['GET'])
def getUnfin():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==False)).all()
    listToOutput = [{"id":task.id, "title":task.title, "time":task.timestamp, "isDone":task.isDone} for task in tasks]
    return jsonify({'status': 200, 'message': 'Ok', 'data': listToOutput})

# 删 某一事项
@app.route('/todolist/task/delete/one/<task_id>', methods=['DELETE'])
def deleteOne(task_id):
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    deleting_task = Task.query.get(task_id)
    db.session.delete(deleting_task)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 删 已完成事项
@app.route('/todolist/task/delete/fin', methods=['DELETE'])
def deleteFin():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==True)).all()
    for task in tasks:
        db.session.delete(task)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 删 未完成事项
@app.route('/todolist/task/delete/unFin', methods=['DELETE'])
def deleteUnfin():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==False)).all()
    for task in tasks:
        db.session.delete(task)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 删 所有事项
@app.route('/todolist/task/delete/all', methods=['DELETE'])
def deleteAll():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter_by(userId=currentId).all()
    for task in tasks:
        db.session.delete(task)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 改 某一事项为已完成
@app.route('/todolist/task/setDone/one/<task_id>', methods=['PUT'])
def setDoneOne(task_id):
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    setting_task = Task.query.get(task_id)
    setting_task.isDone = True
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 改 某一事项为未完成
@app.route('/todolist/task/setUndone/one/<task_id>', methods=['PUT'])
def setUndoneOne(task_id):
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    setting_task = Task.query.get(task_id)
    setting_task.isDone = False
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 改 所有未完成事项为已完成
@app.route('/todolist/task/setDone/all', methods=['PUT'])
def setDoneAll():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==False)).all()
    for task in tasks:
        task.isDone = True
        db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 改 所有已完成事项为未完成
@app.route('/todolist/task/setUndone/all', methods=['PUT'])
def setUndoneAll():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    tasks = Task.query.filter(and_(Task.userId==currentId,Task.isDone==True)).all()
    for task in tasks:
        task.isDone = False
        db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok'})

# 用户 新增id 无密码
@app.route('/todolist/user/new', methods=['POST'])
def newUser():
    newUser = User()
    db.session.add(newUser)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Ok', 'data': newUser.id})

# 用户 无密码登录
@app.route('/todolist/user/login', methods=['GET'])
def loginUser():
    if not request.json or not 'id' in request.json:
        abort(400)
    current_token = token.createToken(request.json['id'])
    return jsonify({'status': 200, 'message': 'Ok', 'token': current_token})

# 查询历史记录
@app.route('/todolist/task/history', methods=['GET'])
def getHistoryTo():
    currentId = token.checkAuth(request)
    if not currentId:
        abort(401)
    return jsonify({'status': 200, 'message': 'Ok', 'data': redis.getHistory(currentId)})
