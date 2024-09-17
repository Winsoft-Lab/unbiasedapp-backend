from flask import Blueprint

api = Blueprint("api", __name__)

from . import (
    errors,
    authentication,
    decorators,
    get_routes,
    get_views,
    post_routes,
    post_views,
    tokens,
)
