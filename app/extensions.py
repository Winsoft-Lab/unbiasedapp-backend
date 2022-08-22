#from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_autodoc.autodoc import Autodoc
from authlib.integrations.flask_client import OAuth
#from pymongo import MongoClient


#client = MongoClient(os.environ.get("MONGO_URI"))

cors = CORS() #Allows for javascript fetch api to access route
mail=Mail() 
db= SQLAlchemy()
auto = Autodoc()
oauth = OAuth()

#db2=client.get_database('test')

#mongo = PyMongo()
login_manger=LoginManager()
login_manger.login_view='auth.login'

