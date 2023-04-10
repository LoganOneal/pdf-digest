
import os 
from apps.extensions import db, login_manager
from celery import Celery 
from flask import Flask
from flask_cors import CORS
from importlib import import_module
from apps.config import config_dict

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('main', 'authentication', 'dashboard', 'api'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_celery_app(app=None):
    # WARNING: Don't run with debug turned on in production!
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # The configuration
    get_config_mode = 'Debug' if DEBUG else 'Production'

    app_config = config_dict[get_config_mode.capitalize()]
    app = app or create_app(app_config)
    celery = Celery(__name__, broker='redis://localhost:6379')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # CORS setup
    CORS(app) 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    register_extensions(app)
    register_blueprints(app)

    from apps.authentication.oauth import github_blueprint
    app.register_blueprint(github_blueprint, url_prefix="/login") 
    
    configure_database(app)

    return app
