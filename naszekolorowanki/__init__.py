import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_env=''):
    app = Flask(__name__)

    if not config_env:
        config_env = app.env
    app.config.from_object(f'config.{config_env.capitalize()}Config')

    login_manager.session_protection = "strong"
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from naszekolorowanki.views.auth_views import bp_auth
        app.register_blueprint(bp_auth)

        from naszekolorowanki.views.image_views import bp_image
        app.register_blueprint(bp_image)

        from naszekolorowanki.views.main_views import bp_main
        app.register_blueprint(bp_main)

    db.init_app(app)

    Migrate(app, db)

    return app
