from flask import Flask
from .extensions import mail, login_manger, db, cors, oauth
from config import config
from celery import Celery
from redis import Redis
import rq

celery_app = Celery(__name__)
# celery = Celery(__name__)
celery_app.conf.broker_read_url = (
    "redis://localhost:6379/"  #'pyamqp://Akachi:12345Akachi@localhost:5672/flask_host'
)
celery_app.conf.broker_write_url = "redis://localhost:6379/0"
# celery_app.conf.result_backend = "pyamqp://Akachi:12345Akachi@localhost:5672/flask_host"


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config["SSL_REDIRECT"]:
        from flask_sslify import SSLify

        sslify = SSLify(app)

    celery_app.conf.update(app.config)

    # REDIS INTEGRATION

    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue("unbiasedapp-tasks", connection=app.redis)

    # EXTENSIONS INITIALIZATION
    login_manger.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    # auto.init_app(app)
    oauth.init_app(app)

    # mongo.init_app(app, )

    # client.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .stripe import stripe as stripe_blueprint

    app.register_blueprint(stripe_blueprint, url_prefix="/stripe")

    from .paypal import paypal as paypal_blueprint

    app.register_blueprint(paypal_blueprint, url_prefix="/paypal")

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    from .errors import error as error_bp

    app.register_blueprint(error_bp)

    return app
