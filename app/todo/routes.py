from flask import jsonify, request
from app.todo import bp
from app.extensions import db
from app.models.todo import Todo
import datetime

@bp.route('/', methods = ['GET'])
def read_all_todos():
  todos = Todo.query.all()
  return jsonify({
    'data': [todo.serialized for todo in todos]
  }), 200

@bp.route('/', methods = ['POST'])
def create_new_todo():
  new_todo = Todo(title=request.form['title'],description=request.form['description'],duedate=datetime.datetime.fromisoformat(request.form['duedate']),status=0,user_id=1)
  db.session.add(new_todo)
  db.session.commit()
  return jsonify({
    'data': new_todo.serialized
  }), 201

@bp.route('/<id>', methods = ['GET'])
def read_single_todo(id):
  res = Todo.query.get(id)
  return (jsonify({
    'data': res.serialized
  }), 200) if res else (jsonify(), 404)

@bp.route('/<id>', methods = ['PUT'])
def update_single_todo(id):
  current_todo = Todo.query.get(id)

  if not current_todo: return jsonify(), 404

  if 'title' in request.form:
    current_todo.title = request.form['title']
  if 'description' in request.form:
    current_todo.description = request.form['description']
  if 'duedate' in request.form:
    current_todo.duedate = datetime.datetime.fromisoformat(request.form['duedate'])
  if 'status' in request.form:
    current_todo.status = request.form['status']
  db.session.commit()
  return jsonify({
    'data': current_todo.serialized
  }), 200

@bp.route('/<id>', methods = ['DELETE'])
def delete_single_todo(id):
  old_todo = Todo.query.get(id)

  if not old_todo: return jsonify(), 404
  
  db.session.delete(old_todo)
  db.session.commit()
  return jsonify({
    'data': old_todo.serialized
  }), 200