from app.api import post_routes
from flask import request
from app.api.authentication import token_auth
from . import api


@api.route("/search-tweet/<string:q>/<int:count>", methods=["POST"])
@token_auth.login_required
def search_tweet(q, count=100):
    # TODO The input has to come from a form
    # q = request.form.get('search_query')
    # count = request.form.get('count')

    return post_routes.search_tweet(q, count)


@api.route("/amazon/<string:product_name>/<string:product_id>", methods=["POST"])
@token_auth.login_required
def amazon_search(product_name, product_id):
    # TODO The input has to come from a form
    # product_name = request.form.get('product_name')
    # product_id = request.form.get('product_id')

    return post_routes.selenium_amazon(product_name, product_id)


@api.route("/jumia/<string:product_id>", methods=["POST"])
@token_auth.login_required
def jumia_search(product_id):
    # TODO The input has to come from a form
    # product_id = request.form.get('product_id')
    return post_routes.selenium_jumia(product_id)


@api.route("/konga/<string:product_name_code_url>", methods=["POST"])
@token_auth.login_required
def konga_search(product_name_code_url):
    # TODO The input has to come from a form
    # product_name_code_url = request.form.get('product_name_code_url')

    return post_routes.selenium_konga(product_name_code_url)


@api.route("/instagram/hashtag-search/<string:q>", methods=["POST"])
@token_auth.login_required
def instagram_hashtag(q):
    # TODO The input has to come from a form
    # q= request.form.get('q')
    return post_routes.instagram_hashtag(q)


@api.route(
    "/facebook/post-comments/<string:page_id>/<string:post_id>", methods=["POST"]
)
@token_auth.login_required
def facebook_page_post(page_id, post_id):
    """_Facebook Page post Comments retrival and storage in database_

    Args:
        page_id (_str_): _description_
        post_id (_str_): _description_

    Returns:
        _type_: _description_

    """

    # TODO Request from  Javascript or Ajax with dynamically assigned values

    return post_routes.facebook_page_post_comments(page_id, post_id)


@api.route(
    "/instagram/comments/<string:fb_page_id>/<string:insta_post_id>/", methods=["POST"]
)
@token_auth.login_required
def instagram_comments(fb_page_id, insta_post_id):
    """_summary_

    Args:
        fb_page_id (_type_): _description_
        insta_post_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return post_routes.instagram_comments(fb_page_id, insta_post_id)
