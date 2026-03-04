from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:shardul99@localhost/flask_db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
#CRUD operations
    
#1) Create
@app.route('/add/<task_name>')
def add_task(task_name):
    
    user = User.query.first()
    
    if not user:
        user = User(name='User1')
        db.session.add(user)
        db.session.commit()
    
    new_task = Task(title = task_name, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()
    
    return f'Added : {task_name} to the database! for User ID {user.id}!'

#2) Read
@app.route('/tasks')
def get_task():
    all_tasks = Task.query.all()
    task_list = []
    
    for task in all_tasks:
        status = "Done" if task.completed else "Pending"
        task_list.append(f"{task.id}. {task.title} - [{status}]")
        
    return "<br>".join(task_list) or "No tasks found!"

#3) Update
@app.route('/complete/<int:task_id>')
def update_task(task_id):
    
    task = Task.query.get(task_id)
    if not task:
        return "Task not found"
    
    task.completed = True
    db.session.commit()
    
    return f'Task {task_id} marked as Complete'

#4) Delete
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    
    task = Task.query.get(task_id)
    
    if not task:
        return "Task not found"
    
    db.session.delete(task)
    db.session.commit()
    
    return f"Task {task_id} deleted successfully!"