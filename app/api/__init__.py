from flask import Blueprint

api = Blueprint('api',__name__)

from . import errors, authentication, decorators, postRoutes, postViews, getRoutes, getViews