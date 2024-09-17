from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from ..models import User
from flask import g
from .errors import error_response
from . import api


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@api.before_app_first_request
@basic_auth.login_required
def before_request():
    if (
        not basic_auth.current_user().is_anonymous
        and not basic_auth.current_user().confirmed
    ):
        return error_response(401, message="Unconfirmed account")


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


@basic_auth.error_handler
def auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


# @api.route("/token/", methods=["POST"])
# def get_token():
#     if g.current_user.is_anonymous or g.token_used:
#         return unauthenticated("Invalid credentials")

#     return jsonify(
#         {
#             "token": g.current_user.generate_auth_token(expiration=3600),
#             "expiration": 3600,
#         }
#     )


# @basic_auth.verify_password
# def verify_password(email_or_token, password):
#     if email_or_token == "":
#         return False
#     if password == "":
#         g.current_user = User.verify_auth_token(email_or_token)
#         g.token_used = True
#         return g.current_user is not None

#     user = User.query.filter_by(email=email_or_token).first()

#     if not user:
#         return False

#     g.current_user = user
#     g.token_used = False

#     return user.verify_password(password)
