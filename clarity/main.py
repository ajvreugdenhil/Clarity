from flask.helpers import send_file
from clarity.models import Task, Event
from flask import Blueprint, render_template, send_from_directory, send_file
from flask_login import login_required, current_user
from . import db
import datetime

from . import create_app

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
        timestamps = []
        for event in allevents:
            if event.task_id == task.id:
                timestamps.append(
                    datetime.datetime.timestamp(event.timestamp)*1000)

        newtask["event_timestamps"] = timestamps
        alltasks.append(newtask)

    return render_template('home.html', tasks=alltasks, graph_max=30)


@ main.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@ main.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@ main.route('/favicon.ico')
def send_favicon():
    return send_file('favicon.ico')

