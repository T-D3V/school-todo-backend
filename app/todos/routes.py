from flask import jsonify
from app.todos import bp

@bp.route('/')
def index():
  return jsonify('This is the api for the todo app!'), 200