from flask import jsonify, current_app, request
from app.main import bp


@bp.route('/')
def index():
  current_app.logger.info(
    f'[{request.remote_addr}][200]: This is the api for the todo app!'
  )
  return jsonify('This is the api for the todo app!'), 200


@bp.route('/health')
def health():
  current_app.logger.info(f"[{request.remote_addr}][200]: It's alive!!!")
  return jsonify("It's alive!!!"), 200
