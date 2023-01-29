from flask import Flask

from config import Config
from app.extensions import db, guard, cors
from app.models.user import User
from flask_login import LoginManager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    guard.init_app(app, User)
    cors.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(main_bp, url_prefix='/')

    # Add users for the example
    with app.app_context():
        db.create_all()
        if db.session.query(User).filter_by(email='user123@test.com').count() < 1:
            db.session.add(User(
            email='user123@test.com',
            password=guard.hash_password('password123'),
            roles='admin'
            ))
        db.session.commit()

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app