from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage
tasks = []

# Helper function to find a task by its ID
def find_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# Helper function to generate a unique ID for a task
def generate_task_id():
    if len(tasks) == 0:
        return 1
    else:
        return tasks[-1]['id'] + 1

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    status = data.get('status', 'Incomplete')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = {
        'id': generate_task_id(),
        'title': title,
        'description': description,
        'due_date': due_date,
        'status': status
    }

    tasks.append(task)
    return jsonify(task), 201

# Retrieve a single task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task:
        return jsonify(task)
    else:
        return jsonify({'error': 'Task not found'}), 404

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if task:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status')

        if title:
            task['title'] = title
        if description:
            task['description'] = description
        if due_date:
            task['due_date'] = due_date
        if status:
            task['status'] = status

        return jsonify(task)
    else:
        return jsonify({'error': 'Task not found'}), 404

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if task:
        tasks.remove(task)
        return jsonify({'message': 'Task deleted'})
    else:
        return jsonify({'error': 'Task not found'}), 404

# List all tasks with pagination
@app.route('/tasks', methods=['GET'])
def list_tasks():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    start = (page - 1) * per_page
    end = start + per_page

    paginated_tasks = tasks[start:end]
    return jsonify(paginated_tasks)

if __name__ == '__main__':
    app.run(debug=True)
