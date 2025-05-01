from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app.auth import token_required


main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = user.generate_token()
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@main.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

@main.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'is_done': task.is_done
        })
    return jsonify({'tasks': result}), 200

@main.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.is_done = data.get('is_done', task.is_done)

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200

@main.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200

