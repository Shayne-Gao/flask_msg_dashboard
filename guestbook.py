#!/usr /bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jiangge'

import shelve
import random
from datetime import datetime
from flask import Flask, request, render_template, redirect
from user_agents import parse
# pip install pyyaml ua-parser user-agents
# https://github.com/selwin/python-user-agents

application = Flask(__name__)

DATA_FILE = 'db.dat'


def save_data(name, gender, comment, create_at):
    """
    save data from form submitted
    """
    database = shelve.open(DATA_FILE)

    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']

    greeting_list.insert(
        0, {'name': name, 'gender':gender, 'comment': comment, 'create_at': create_at})

    database['greeting_list'] = greeting_list

    database.close()


def load_data():
    """
    load saved data
    """
    database = shelve.open(DATA_FILE)

    greeting_list = database.get('greeting_list', [])

    database.close()

    return greeting_list


@application.route('/')
def index():
    """Top page
    Use template to show the page
    """
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)


@application.route('/post', methods=['POST'])
def post():
    """Comment's target url
    """
    #name = request.form.get('name')
    userAgent = parse(request.user_agent.string)
    with open('randname.data', 'r') as f:
    	lines = f.readlines()
    	random_line = random.choice(lines)
    if userAgent.device.model == 'iPhone':
        name = random_line 
        gender = 0 
    elif userAgent.device.model == 'M2007J1SC':
        name = random_line
        gender = 1
    else:
        name = userAgent
        gender = -1
    comment = request.form.get('comment')
    create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_data(name, gender, comment, create_at)

    return redirect('/')


if __name__ == '__main__':
    application.run('0.0.0.0', port=80, debug=False)
