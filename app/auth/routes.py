from flask import jsonify
from app.auth import bp

@bp.route('/')
def index():
  return jsonify('This is the api for the todo app!'), 200