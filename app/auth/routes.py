from flask import jsonify, request, current_app, make_response
from app.auth import bp
from app.models.user import User
import bcrypt
from app.extensions import db
from app.models.role import ROLES, Role
import jwt
from app.auth.decorators import token_required
from datetime import datetime, timezone, timedelta
import re


@bp.route('/register', methods=['POST'])
def register():
  username = request.json.get('username')
  password = request.json.get('password')

  if not username:
    return jsonify({'message': 'No username provided!'}), 400

  if not password:
    return jsonify({'message': 'No password provided!'}), 400

  if not re.fullmatch(r'^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$', username):
    return jsonify({'message': "The username doesn't meet the requirements!"}), 400

  if len(password) < 8:
    return jsonify({'message': 'The password must be at least 8 characters long!'}), 400

  if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
    return jsonify({'message': "The password didn't meet the requirements!"}), 400

  existing_user = User.query.filter_by(username=username).first()
  if existing_user:
    return jsonify({'message': 'This Username is already taken!'}), 400

  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  new_user = User(username=username, password=hashed_password, role_id=ROLES['user'])
  db.session.add(new_user)
  db.session.commit()

  return (
    jsonify({'message': 'User registerd successfully.', 'data': {new_user.serialized}}),
    201,
  )


@bp.route('/login', methods=['POST'])
def login():
  username = request.json.get('username')
  password = request.json.get('password')

  if not username:
    return jsonify({'message': 'No username provided!'}), 400

  if not password:
    return jsonify({'message': 'No password provided!'}), 400

  user = User.query.filter_by(username=username).first()
  if user:
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
      token = jwt.encode(
        {
          'user_id': str(user.id),
          'username': user.username,
          'role': str(user.role_id),
          'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=3600),
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256',
      )

      response = make_response(jsonify({'message': 'Login successful.'}), 200)
      response.set_cookie('token', token)
      return response
  return jsonify({'message': 'Invalid username or password!'}), 400


@bp.route('/user', methods=['GET'])
@token_required
def read_all_users(current_user: User):
  if ROLES['user'] == current_user.role_id:
    return (
      jsonify({'message': "You don't have access to the selected resource!"}),
      403,
    )
  users = User.query.all()
  return (
    jsonify(
      {
        'message': 'Successfully gathered all users.',
        'data': {[user.serialized for user in users]},
      }
    ),
    200,
  )


@bp.route('/user/<id>', methods=['GET'])
@token_required
def read_single_user(id, current_user: User):
  selected_user = User.query.get(id)
  if not selected_user:
    return jsonify({'message': "The requested user doesn' exist!"}), 404
  if ROLES['user'] == current_user.role_id and id != current_user.id:
    return jsonify({'message': "You don't have access to the requested user!"}), 403
  return (
    jsonify(
      {
        'message': 'Successfully gathered user information.',
        'data': {selected_user.serialized},
      }
    ),
    200,
  )


@bp.route('/user/<id>', methods=['PATCH'])
@token_required
def update_single_user(current_user: User, id):
  selected_user = User.query.get(id)
  if not selected_user:
    return jsonify({'message': "The requested user doesn' exist!"}), 404
  if ROLES['user'] == current_user.role_id and id != current_user.id:
    return jsonify({'message': "You don't have access to the requested user!"}), 403
  username = request.json.get('username')
  old_password = request.json.get('old_password')
  new_password = request.json.get('new_password')
  role_id = request.json.get('role_id')

  if not username and not old_password and not new_password and not role_id:
    return jsonify({'message': 'Nothing to alter!'}), 201

  if username and not re.fullmatch(r'^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$', username):
    return jsonify({'message': "The username doesn't meet the requirements!"}), 400

  if new_password and len(new_password) < 8:
    return jsonify({'message': 'The password must be at least 8 characters long!'}), 400

  if new_password and not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', new_password):
    return jsonify({'message': "The password didn't meet the requirements!"}), 400

  existing_user = User.query.filter_by(username=username).first()
  if existing_user:
    return jsonify({'message': 'This Username is already taken!'}), 400

  if role_id and not Role.query.filter_by(id=role_id).first():
    return jsonify({'message': "The provided role doesn't exist!"}), 400
  if username:
    selected_user.username = username
  if new_password:
    if ROLES['admin'] == current_user.role_id:
      selected_user.password = bcrypt.hashpw(
        new_password.encode('utf-8'), bcrypt.gensalt()
      )
    else:
      if old_password:
        if bcrypt.checkpw(old_password.encode('utf-8'), selected_user.password):
          selected_user.password = bcrypt.hashpw(
            new_password.encode('utf-8'), bcrypt.gensalt()
          )
        else:
          return (
            jsonify({'message': 'The request contained invalid data!'}),
            400,
          )
      else:
        return jsonify({'message': 'The request is missing data!'}), 400
  if role_id:
    if ROLES['admin'] == current_user.role_id:
      selected_user.role_id = role_id
    else:
      return jsonify({'message': "You aren't authorized to do this!"}), 403
  db.session.commit()
  return (
    jsonify(
      {
        'message': 'User was succesfully altered',
        'data': selected_user.serialized,
      }
    ),
    200,
  )


@bp.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_single_user(current_user: User, id):
  selected_user = User.query.get(id)
  if not selected_user:
    return jsonify({'message': "The requested user doesn' exist!"}), 404
  if ROLES['user'] == current_user.role_id and id != current_user.id:
    return jsonify({'message': "You don't have access to the requested user!"}), 403
  db.session.delete(selected_user)
  db.session.commit()
  return (
    jsonify(
      {
        'message': 'User was successfully delted.',
        'data': {'user_id': selected_user.id},
      }
    ),
    200,
  )
