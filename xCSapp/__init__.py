import os
from flask import g
from flask import Flask
import sqlite3
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/usrank')
    def usrank():
        data = load_json_data('school.json')  # 读取 JSON 数据
        us_data = data.get('us', {})  # 获取 'us' 键的内容
        return render_template('usrank.html', data=us_data)

    @app.route('/globalrank')
    def carank():
        data = load_json_data('global.json')  # 读取 JSON 数据
        return render_template('globalrank.html', data=data)

    @app.route('/visa')
    def visa():
        return render_template('visa.html')

    @app.route('/cvsop')
    def cvsop():
        return render_template('cvsop.html')

    @app.route('/writing')
    def writing():
        return render_template('writing.html')
    
    @app.route('/business')
    def business():
        return render_template('business.html') 

    from . import db
    db.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app

def load_json_data(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)  # 假设 JSON 文件放在 'data' 文件夹中
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}  