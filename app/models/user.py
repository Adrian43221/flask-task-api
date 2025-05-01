from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expires_in=3600):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }

        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return token

    def __repr__(self):
        return f"<User {self.username}>"