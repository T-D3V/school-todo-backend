import os
from app.models.user import User
from app.models.role import Role
from app.extensions import db
import click
from flask.cli import with_appcontext

def populate_db():
  admin_role = Role(name= 'admin')
  db.session.add(admin_role)
  db.session.flush()
  admin_user = User(username= os.getenv('ADMIN_USER') if os.getenv('ADMIN_USER') else 'admin', password = os.getenv('ADMIN_PASSWORD') if os.getenv('ADMIN_PASSWORD') else 'admin', role_id = admin_role.id)
  db.session.add(admin_user)
  db.session.commit()
  
@click.command('pre-populate')
@with_appcontext
def populate_db_command():
  populate_db()

