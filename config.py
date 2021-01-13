import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or b'\x8aP\xb5y\x19\xa6S\xd4\xa6+\xed\xed\r\xc3\x06\xa8'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_IMAGE_EXTENSIONS = ["jpeg", "jpg", "png"]
    USER_NAME = "naszadmin"
    USER_PASSWORD = 'Naszehaslo1!'



class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "naszekolorowanki", "app.db")}'
    IMAGE_UPLOADS = os.path.join(basedir, "naszekolorowanki", "uploaded_pictures")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "test.sqlite")}'
    IMAGE_UPLOADS = os.path.join(basedir, "naszekolorowanki", "uploaded_pictures")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "FLASK_DB_URI") or f'sqlite:///{os.path.join(basedir, "naszekolorowanki", "app.db")}'
    IMAGE_UPLOADS = os.environ.get("FLASK_UPLOADS_FOLDER_URI") or os.path.join(basedir, "naszekolorowanki",
                                                                               "uploaded_pictures")
