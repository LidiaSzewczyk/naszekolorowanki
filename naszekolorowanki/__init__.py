import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'\x93\xb4\xbf\xdc\x83\x86\x00\xcc\xce\x01WZ\xb9\xa8\xe1E'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")}'

    from naszekolorowanki.views.main_views import bp_main
    from naszekolorowanki.views.auth_views import bp_auth
    from naszekolorowanki.views.image_views import bp_image

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_image)

    login_manager.session_protection = "strong"
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.init_app(app)

    Migrate(app, db)

    return app
