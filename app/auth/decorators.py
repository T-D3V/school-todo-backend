from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models.user import User

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get('token')
    if not token:
      return jsonify({'message': 'No authentication provided!'}), 401
    
    try:
      data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
      current_user = User.query.get(data['user_id'])
    except jwt.ExpiredSignatureError:
      return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
      return jsonify({'message': 'Invalid token!'}), 401
    
    return f(current_user=current_user, *args, **kwargs)
  return decorated