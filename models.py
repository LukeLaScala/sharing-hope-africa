import bcrypt

from sharing import db, login_manager
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(length=128), unique=True)

    email = db.Column(db.Unicode(length=128), unique=True)
    confirmed_email = db.Column(db.Boolean, default=False)

    # bcrypt
    password = db.Column(db.String(length=80))

    admin = db.Column(db.Boolean, default=False)

    joined = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.admin
    
    def get_email(self):
        return self.email

    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password:

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_pw(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    @staticmethod
    def login(username, password):
        u = User.query.filter_by(username=username).first()
        if u is None:
            return False

        return u.check_password(password)

    @staticmethod
    def register(username, password, email):
        if User.query.filter_by(username=username).count() != 0:
            return "This username has been taken by another user."

        u = User(username=username, password=User.hash_pw(password), email=email)
        u.save()

        return True

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
