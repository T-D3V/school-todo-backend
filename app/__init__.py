from flask import Flask
from config import Config
from app.extensions import db, cors

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  # Initialize Flask extensions here
  cors.init_app(app, resources=r'/*')
  db.init_app(app)

  # Register blueprints here
  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix='/auth')

  from app.todo import bp as todo_bp
  app.register_blueprint(todo_bp, url_prefix='/todo')
  
  from app.todos import bp as todos_bp
  app.register_blueprint(todos_bp, url_prefix='/todos')

  return app
