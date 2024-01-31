from flask import Flask
from config import Config
from app.extensions import db, cors, migrate, formatter
import logging


def create_app(config_class=Config):
  app = Flask(__name__)
  if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.addHandler(logging.FileHandler('/app/log/todo_api.log'))
    for handler in app.logger.handlers:
      handler.setFormatter(formatter)
    app.logger.setLevel(gunicorn_logger.level)

  app.config.from_object(config_class)

  # Initialize Flask extensions here
  cors.init_app(app, resources=r'/*')
  db.init_app(app)
  migrate.init_app(app, db, command='migrate')
  app.logger.info('Logging initialized')

  # Register blueprints here
  from app.main import bp as main_bp

  app.register_blueprint(main_bp)

  from app.auth import bp as auth_bp

  app.register_blueprint(auth_bp, url_prefix='/auth')

  from app.todo import bp as todo_bp

  app.register_blueprint(todo_bp, url_prefix='/todo')

  from app.models import todo, user, role, todo_security, user_security, role_security

  from db_setup import populate_db_command

  app.cli.add_command(populate_db_command)

  return app
