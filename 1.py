from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Задача добавлена успешно'})
    else:
        return jsonify({'message': 'Ошибка: ожидался JSON-формат'})

@app.route('/update_task/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        if request.is_json:
            data = request.get_json()
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.done = data.get('done', task.done)
            db.session.commit()
            return jsonify({'message': 'Задача обновлена успешно'})
        else:
            return jsonify({'message': 'Ошибка: ожидался JSON-формат'})
    else:
        return jsonify({'message': 'Задача не найдена'})

@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Задача удалена успешно'})
    else:
        return jsonify({'message': 'Задача не найдена'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
