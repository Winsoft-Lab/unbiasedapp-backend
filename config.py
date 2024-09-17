import os

# os.environ.setdefault('FORKED_BY_MULTIPROCESSING','1')
basedir = os.path.dirname(os.path.abspath(__file__))


class Config:
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.mail.yahoo.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 465))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "Akachi")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = "Unbiased Analytics|"
    MAIL_SENDER = os.environ.get("MAIL_SENDER", "anabantiakachi@yahoo.com")
    SERVER_ADMIN = os.environ.get("SERVER_ADMIN", "Akachi")
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME='localhost:5000'
    TWITTER_SECRET = os.environ.get("TWITTER_SECRET")
    TWITTER_KEY = os.environ.get("TWITTER_KEY")
    FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET")
    CORS_HEADERS = "Content-Type"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:6379/"  # "redis://localhost:6379" #'pyamqp://Akachi:12345Akachi@localhost:5672/flask_host'
    result_backend = "redis://redis:6379"  #'rpc://'
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
    SSL_REDIRECT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopementSetting(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingSetting(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionSetting(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email error to the admin
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.SERVER_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + "Application",
            credentials=credentials,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuSetting(ProductionSetting):

    SSL_REDIRECT = True if os.environ.get("DYNO") else False

    @classmethod
    def init_app(cls, app):
        ProductionSetting.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # handling reverse proxy server headers
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    "development": DevelopementSetting,
    "testing": TestingSetting,
    "production": ProductionSetting,
    "heroku": HerokuSetting,
    "default": DevelopementSetting,
}
