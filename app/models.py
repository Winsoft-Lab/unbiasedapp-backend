import os
import base64
from datetime import datetime, timedelta
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from .extensions import db, login_manger
from werkzeug.security import generate_password_hash, check_password_hash
import redis
import rq

# TODO replace the TimedJSONWebSignatureSerializer with jwt
# import jwt


class StripeCustomer(db.Model):
    __tablename__ = "stripe_customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    StripeCustomerId = db.Column(db.String(255), nullable=False)
    StripeSubscriptionId = db.Column(db.String(255), nullable=False, unique=True)


# --------------------SOCIAL MODELS--------------------------
class TwitterAnalysis(db.Model):
    __tablename__ = "twitter_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    search_query = db.Column(db.String(255), nullable=False, unique=True)
    tweets = db.Column(db.String)


class FacebookAnalysis(db.Model):
    __tablename__ = "facebook_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    fb_page = db.Column(db.String(255), db.ForeignKey("users.fb_page_id"))
    fb_post_id = db.Column(db.String)
    comments = db.Column(db.String)


class InstagramAnalysis(db.Model):
    __tablename__ = "instagram_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fb_page = db.Column(db.String(255), db.ForeignKey("users.fb_page_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    insta_post_id = db.Column(db.String(255), nullable=False, unique=True)
    comments = db.Column(db.String)


# class InstagramHastagAnalysis(db.models):
#     __tablename__ = 'instagram_hashtag_analysis'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     hashtg = db.Column(db.String(255))
#     posts = db.Column(db.String)

# ---------------------ECOMMERCE MODELS--------------------------
class AmazonAnalysis(db.Model):
    __tablename__ = "amazon_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    product_id = db.Column(db.String(255), nullable=True)
    product_name = db.Column(db.String(255), nullable=True)
    reviews = db.Column(db.String)


class JumiaAnalysis(db.Model):
    __tablename__ = "jumia_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    product_id = db.Column(db.String(255), nullable=False)
    reviews = db.Column(db.String)


class KongaAnalysis(db.Model):
    __tablename__ = "konga_analysis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=None)
    product_description = db.Column(db.String(255), nullable=True)
    reviews = db.Column(db.String)


# ------------------------USER MODEL---------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # uid = db.Column(db.string(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=True)
    fb_access_token = db.Column(db.String)
    fb_page_id = db.Column(db.String(128))

    # User data analyses
    # jumia_analysis = db.relationship("JumiaAnalysis", backref="users")
    # konga_analysis = db.relationship("KongaAnalysis", backref="users")
    # amazon_analysis = db.relationship("AmazonAnalysis", backref="users")
    # facebook_analysis = db.relationship("FacebookAnalysis", backref="users")
    # instagram_analysis = db.relationship("InstagramAnalysis", backref="users")

    # API tokens and verification
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # TASKS MANGER
    tasks = db.relationship("Task", backref="users", lazy="dynamic")

    def get_token(self, expires_in=7200):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    # --------------------------------

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=7200):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False

        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["id"])

    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_enqueue("app.tasks." + name, self.id, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_task_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.query.filter_by(name=name, user=self, complete=False).first()


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get("progress", 0) if job is not None else 100


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
