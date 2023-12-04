import os
from app.models.user import User
from app.models.role import Role
from app.extensions import db
import click
from flask.cli import with_appcontext
import bcrypt

def populate_db():
  admin_role = Role(name= 'admin')
  db.session.add(admin_role)
  user_role = Role(name= 'user')
  db.session.add(user_role)
  db.session.flush()
  admin_user = User(username= os.environ.get('ADMIN_USER', 'admin'), password = bcrypt.hashpw(os.environ.get('ADMIN_PASSWORD', 'admin').encode('utf-8'), bcrypt.gensalt()), role_id = admin_role.id)
  db.session.add(admin_user)
  db.session.commit()
  
@click.command('pre-populate')
@with_appcontext
def populate_db_command():
  populate_db()

