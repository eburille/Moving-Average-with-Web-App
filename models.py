from sqlalchemy import ForeignKey
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(75), unique = True, index = True)
    email = db.Column(db.String(100), unique = True, index = True)
    password_hash = db.Column(db.String(300))
    acoes = db.relationship('lista_de_acoes', backref='lista_de_acoes', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

class lista_de_acoes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    acao = db.Column(db.String(5), index = False, unique = False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

@login.user_loader
def load_user(id):
  return User.query.get(int(id))