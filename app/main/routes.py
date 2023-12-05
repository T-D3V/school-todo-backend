from flask import jsonify
from app.main import bp


@bp.route('/')
def index():
  return jsonify('This is the api for the todo app!'), 200


@bp.route('/health')
def health():
  return jsonify("It's alive!!!"), 200
