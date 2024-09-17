from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

# from flask_autodoc import Autodoc
from authlib.integrations.flask_client import OAuth

cors = CORS()  # Allows for javascript fetch api to access route
mail = Mail()
db = SQLAlchemy()
# auto = Autodoc()
oauth = OAuth()

login_manger = LoginManager()
login_manger.login_view = "auth.login"
