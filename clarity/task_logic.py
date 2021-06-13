from clarity.models import Task, Event
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db
import datetime

task_logic = Blueprint('task_logic', __name__)


@ task_logic.route('/task_config')
@ login_required
def task_config():
    user_id = current_user.id
    all_tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('task_config.html', tasks=all_tasks)


@ task_logic.route('/event_config', methods=['POST'])
@ login_required
def event_config():
    task_id = request.form.get('task_id')
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id, task_id=task_id).all()
    event_count = len(events)
    return render_template('event_config.html', events=events, event_count=event_count)


@ task_logic.route('/add_task', methods=['POST'])
@ login_required
def config_add_task():
    user_id = current_user.id
    task_name = request.form.get('task_name')
    new_task = Task(user_id=user_id, name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task_logic.task_config'))


@ task_logic.route('/delete_task', methods=['POST'])
@ login_required
def config_delete_task():
    user_id = current_user.id
    task_id = request.form.get('task_id')
    deletee = Task.query.filter_by(user_id=user_id, id=task_id).all()
    if (len(deletee) != 1):
        raise Exception("none or duplicate Tasks to be deleted")
    db.session.delete(deletee[0])
    db.session.commit()
    return redirect(url_for('task_logic.task_config'))


@ task_logic.route('/finished_task', methods=['POST'])
@ login_required
def home_finished_task():
    user_id = current_user.id
    task_id = request.form.get('task_id')
    new_event = Event(task_id=task_id, user_id=user_id,
                      timestamp=datetime.datetime.now())
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('main.home'))

@ task_logic.route('/delete_event', methods=['POST'])
@ login_required
def delete_event():
    user_id = current_user.id
    event_id = request.form.get('event_id')
    deletee = Event.query.filter_by(user_id=user_id, id=event_id).all()
    if (len(deletee) != 1):
        raise Exception("none or duplicate events to be deleted")
    db.session.delete(deletee[0])
    db.session.commit()
    return redirect(url_for('main.home'))
