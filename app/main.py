from app.models import Task, Event
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home')
@login_required
def home():
    user_id = current_user.id
    rawtasks = Task.query.filter_by(user_id=user_id).all()
    allevents = Event.query.filter_by(user_id=user_id).all()
    alltasks = []
    for task in rawtasks:
        newtask = {}
        newtask["id"] = task.id
        newtask["name"] = task.name

        history_length = 21
        labels = [""] * history_length
        values = [0] * history_length

        for i in range(history_length):
            labels[i] = f"-{i}d"
            for event in allevents:
                if (event.task_id == task.id) and (event.timestamp > datetime.datetime.now() - datetime.timedelta(days=i+1)) and (event.timestamp < datetime.datetime.now() - datetime.timedelta(days=i)):
                    values[i] += 1
        newtask["graph_labels"] = labels
        newtask["graph_values"] = values
        alltasks.append(newtask)

    return render_template('home.html', tasks=alltasks, graph_max=30)


@ main.route('/config')
@ login_required
def config():
    user_id=current_user.id
    all_tasks=Task.query.filter_by(user_id=user_id).all()
    return render_template('config.html', tasks=all_tasks)


@ main.route('/add_task', methods=['POST'])
@ login_required
def config_add_task():
    user_id=current_user.id
    task_name=request.form.get('task_name')
    new_task=Task(user_id=user_id, name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.config'))


@ main.route('/delete_task', methods=['POST'])
@ login_required
def config_delete_task():
    user_id=current_user.id
    task_id=request.form.get('task_id')
    deletee=Task.query.filter_by(user_id=user_id, id=task_id).all()
    if (len(deletee) != 1):
        raise Exception
    db.session.delete(deletee[0])
    db.session.commit()
    return redirect(url_for('main.config'))


@ main.route('/finished_task', methods=['POST'])
@ login_required
def home_finished_task():
    user_id=current_user.id
    task_id=request.form.get('task_id')
    new_event=Event(task_id=task_id, user_id=user_id,
                      timestamp=datetime.datetime.now())
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('main.home'))
