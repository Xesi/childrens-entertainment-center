from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import redis
from PIL import Image
import io
import babel
from babel.dates import format_date, format_datetime, format_time
import datetime

import sqlite3

from flask_pymongo import PyMongo

db = SQLAlchemy()

r = redis.StrictRedis(
    host='redis-11643.c265.us-east-1-2.ec2.cloud.redislabs.com',
    port=11643,
    password='JQN92VK86Jx3Pa1jQMxrDB7JLWVxyKyM',
)

def get_db_connection():
    conn = sqlite3.connect('coursework/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
    mongodb_client = PyMongo(app)
    mongodb = mongodb_client.db

    @app.template_filter()
    def format_datetime(value, format='date'):
        date_obj = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if format == 'time':
            return date_obj.strftime("%H:%M")
        elif format == 'date':
            return date_obj.strftime("%d %b %Y")

    app.config['SECRET_KEY'] = 'secret-key-for-coursework'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    try:
        with app.app_context():
            admin = User(name = 'Администратор', admin = True, email = 'admin@gmail.com', password=generate_password_hash("123", method='sha256'))
            db.session.add(admin)
            db.session.commit()
    except:
        pass

    img = open("coursework/static/default.png","rb").read()
    r.set("default", img)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from .news import news_feed as profile_blueprint
    app.register_blueprint(profile_blueprint)


    return app