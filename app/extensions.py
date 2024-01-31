from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging


db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
formatter = logging.Formatter(
  '[%(asctime)s] [%(process)d] [%(levelname)s] [%(pathname)s] %(message)s'
)
