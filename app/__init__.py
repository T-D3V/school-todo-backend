from flask import Flask
from config import Config
from app.extensions import db, cors, migrate


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  # Initialize Flask extensions here
  cors.init_app(app, resources=r'/*')
  db.init_app(app)
  migrate.init_app(app, db, command='migrate')

  # Register blueprints here
  from app.main import bp as main_bp

  app.register_blueprint(main_bp)

  from app.auth import bp as auth_bp

  app.register_blueprint(auth_bp, url_prefix='/auth')

  from app.todo import bp as todo_bp

  app.register_blueprint(todo_bp, url_prefix='/todo')

  from app.models import todo, user, role

  from db_setup import populate_db_command

  app.cli.add_command(populate_db_command)

  return app
