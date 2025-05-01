import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            current_user = User.query.get(user_id)

            if not current_user:
                return jsonify({'error': 'User not found'}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

