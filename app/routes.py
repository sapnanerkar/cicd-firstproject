from flask import Blueprint, jsonify, request
from .models import Task

task_bp = Blueprint('tasks', _name_)
tasks = []
next_id = 1

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': [task.to_dict() for task in tasks]
    })

@task_bp.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_task = Task(id=next_id, name=data['name'])
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task.to_dict()), 201