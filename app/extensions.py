from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging
import logging.handlers
import sys

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
  'flask [%(ascitime)s][%(levelname)s][%(pathname)s]: %(message)s'
)
handler.setFormatter(formatter)
handlerFile = logging.FileHandler('/app/log/todo_api.log')
handlerFile.setFormatter(formatter)
