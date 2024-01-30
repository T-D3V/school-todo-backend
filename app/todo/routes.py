from flask import jsonify, request, current_app
from app.todo import bp
from app.extensions import db
from app.models.todo import Todo
from app.models.todo_security import TodoSecurity
import datetime
from app.auth.decorators import token_required
from app.models.role import ROLES
import html


@bp.route('/', methods=['GET'])
@token_required
def read_all_todos(current_user):
  todos = (
    Todo.query.all()
    if ROLES['admin'] == current_user.role_id
    else Todo.query.filter_by(user_id=current_user.user_id).all()
  )
  current_app.logger.info(
    f'[{request.remote_addr}][200]: Gathered all accessible todos.'
  )
  return jsonify(
    {
      'message': 'Gathered all accessible todos.',
      'data': [todo.serialized for todo in todos],
    }
  ), 200


@bp.route('/', methods=['POST'])
@token_required
def create_new_todo(current_user):
  title = request.json.get('title')
  description = request.json.get('description')
  duedate = request.json.get('duedate')
  user_id = current_user.id

  if not title or not description or not duedate or not user_id:
    current_app.logger.info(
      f'[{request.remote_addr}][400]: To little information provided!'
    )
    return jsonify({'message': 'To little information provided!'}), 400
  if len(title) > 150:
    current_app.logger.info(
      f'[{request.remote_addr}][400]: Title is longer than 150 characters!'
    )
    return jsonify({'message': 'Title is longer than 150 characters!'}), 400
  title = html.escape(title)
  # If one wanted to store escaped html in the database but I would suggest to let frontend handle the escaping maybee one wants to use a wysiwyg editor for description
  # description = html.escape(description)
  try:
    datetime.datetime.fromisoformat(duedate)
  except ValueError:
    current_app.logger.info(
      f"[{request.remote_addr}][400]: The provided date doesn't match ISO8601 requirements!"
    )
    return jsonify(
      {'message': "The provided date doesn't match ISO8601 requirements!"}
    ), 400

  new_todo = Todo(
    title=title,
    description=description,
    duedate=datetime.datetime.fromisoformat(duedate),
    status=0,
    user_id=user_id,
  )
  db.session.add(new_todo)
  db.session.commit()
  new_todo_security = TodoSecurity(
    action='INSERT',
    todo_id=new_todo.id,
    todo_title=new_todo.title,
    todo_description=new_todo.description,
    todo_duedate=new_todo.duedate,
    todo_status=new_todo.status,
    todo_user_id=new_todo.user_id,
    action_by=f'{current_user.id}.{current_user.username}',
  )
  db.session.add(new_todo_security)
  db.session.commit()
  current_app.logger.info(
    f'[{request.remote_addr}][201]: Successfully created a new todo.'
  )
  return jsonify(
    {'message': 'Successfully created a new todo.', 'data': new_todo.serialized}
  ), 201


@bp.route('/<id>', methods=['GET'])
@token_required
def read_single_todo(current_user, id):
  todo = Todo.query.get(id)
  if not todo:
    current_app.logger.info(f'[{request.remote_addr}][404]: There is no such todo!')
    return jsonify({'message': 'There is no such todo!'}), 404
  if ROLES['user'] == current_user.role_id and todo.user_id != current_user.user_id:
    current_app.logger.warn(
      f"[{request.remote_addr}][403]: You don't have access to the requested resource!"
    )
    return jsonify({'message': "You don't have access to the requested resource!"}), 403
  current_app.logger.info(
    f'[{request.remote_addr}][200]: Successfully gathered the requested todo.'
  )
  return jsonify(
    {'message': 'Successfully gathered the requested todo.', 'data': todo.serialized}
  ), 200


@bp.route('/<id>', methods=['PATCH'])
@token_required
def update_single_todo(current_user, id):
  current_todo = Todo.query.get(id)
  if not current_todo:
    current_app.logger.info(f'[{request.remote_addr}][404]: There is no such todo!')
    return jsonify({'message': 'There is no such todo!'}), 404
  if (
    ROLES['user'] == current_user.role_id
    and current_todo.user_id != current_user.user_id
  ):
    current_app.logger.warn(
      f"[{request.remote_addr}][403]: You don't have access to the requested resource!"
    )
    return jsonify({'message': "You don't have access to the requested resource!"}), 403

  title = request.json.get('title')
  description = request.json.get('description')
  duedate = request.json.get('duedate')
  status = request.json.get('status')

  if not title and not description and not duedate and not status:
    current_app.logger.info(
      f"[{request.remote_addr}][400]: The request didn't contain any valid data!"
    )
    return jsonify({'message': "The request didn't contain any valid data!"}), 400

  if len(title) > 150:
    current_app.logger.info(
      f'[{request.remote_addr}][400]: Title is longer than 150 characters!'
    )
    return jsonify({'message': 'Title is longer than 150 characters!'}), 400
  title = html.escape(title)
  # If one wanted to store escaped html in the database but I would suggest to let frontend handle the escaping maybee one wants to use a wysiwyg editor for description
  # description = html.escape(description)
  try:
    datetime.datetime.fromisoformat(duedate)
  except ValueError:
    current_app.logger.info(
      f"[{request.remote_addr}][400]: The provided date doesn't match ISO8601 requirements!"
    )
    return jsonify(
      {'message': "The provided date doesn't match ISO8601 requirements!"}
    ), 400

  # If i would be maintainer of frontend and backend I would also validate status but, this isn't validated here cause I have no knowledge of how many status the todo has,  could be implemented over an environement variable.

  if title:
    current_todo.title = title
  if description:
    current_todo.description = description
  if duedate:
    current_todo.duedate = datetime.datetime.fromisoformat(duedate)
  if status:
    current_todo.status = status

  current_todo_security = TodoSecurity(
    action='UPDATE',
    todo_id=current_todo.id,
    todo_title=current_todo.title,
    todo_description=current_todo.description,
    todo_duedate=current_todo.duedate,
    todo_status=current_todo.status,
    todo_user_id=current_todo.user_id,
    action_by=f'{current_user.id}.{current_user.username}',
  )
  db.session.add(current_todo_security)
  db.session.commit()
  current_app.logger.info(
    f'[{request.remote_addr}][200]: Successfully updated the requested todo.'
  )
  return jsonify(
    {
      'message': 'Successfully updated the requested todo.',
      'data': current_todo.serialized,
    }
  ), 200


@bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_single_todo(current_user, id):
  old_todo = Todo.query.get(id)
  if not old_todo:
    current_app.logger.info(f'[{request.remote_addr}][404]: There is no such todo!')
    return jsonify({'message': 'There is no such todo!'}), 404
  if ROLES['user'] == current_user.role_id and old_todo.user_id != current_user.user_id:
    current_app.logger.warn(
      f"[{request.remote_addr}][403]: You don't have access to the requested resource!"
    )
    return jsonify({'message': "You don't have access to the requested resource!"}), 403
  old_todo_security = TodoSecurity(
    action='DELETE',
    todo_id=old_todo.id,
    action_by=f'{current_user.id}.{current_user.username}',
  )
  db.session.add(old_todo_security)
  db.session.delete(old_todo)
  db.session.commit()
  current_app.logger.info(
    f'[{request.remote_addr}][200]: Successfully delted the requested resource.'
  )
  return jsonify(
    {
      'message': 'Successfully delted the requested resource.',
      'data': old_todo.serialized,
    }
  ), 200
