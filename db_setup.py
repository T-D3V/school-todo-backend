import os
from app.models.user import User
from app.models.role import Role
from app.models.role_security import RoleSecurity
from app.models.user_security import UserSecurity
from app.extensions import db
import click
from flask.cli import with_appcontext
import bcrypt


def populate_db():
  admin_role = Role(name='admin')
  db.session.add(admin_role)
  db.session.commit()
  admin_role_security = RoleSecurity(action='INSERT', role_id=admin_role.id, role_name=admin_role.name, action_by='init_script')
  db.session.add(admin_role_security)
  user_role = Role(name='user')
  db.session.add(user_role)
  db.session.commit()
  user_role_security = RoleSecurity(action='INSERT', role_id=user_role.id, role_name=user_role.name, action_by='init_script')
  db.session.add(user_role_security)
  db.session.flush()
  admin_user = User(
    username=os.environ.get('ADMIN_USER', 'admin'),
    password=bcrypt.hashpw(
      os.environ.get('ADMIN_PASSWORD', 'admin').encode('utf-8'), bcrypt.gensalt()
    ),
    role_id=admin_role.id,
  )
  db.session.add(admin_user)
  db.session.commit()
  admin_user_security = UserSecurity(action='INSERT', user_id=admin_user.id, user_username=admin_user.username, user_role_id=admin_user.role_id, action_by='init_script')
  db.session.add(admin_user_security)
  db.session.commit()


@click.command('pre-populate')
@with_appcontext
def populate_db_command():
  populate_db()
