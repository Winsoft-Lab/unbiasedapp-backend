from app.api.authentication import token_auth, basic_auth
from . import api
from app.api import get_routes


@api.route("/")
@token_auth.login_required
def api_home():
    user = basic_auth.current_user()
    msg = f"Hello {user.username} welcome to unbiased api please read the docs  to get started"
    return {"msg": msg}


@api.route("/get-facebook-pages")
@token_auth.login_required
def show_pages():
    return get_routes.get_facebook_pages()


@api.route("/show-page-posts/<string:page_id>")
@token_auth.login_required
def show_post(page_id):
    return get_routes.get_posts(page_id)


@api.route("/instagram/")
@token_auth.login_required
def get_instagram_analysis():
    """
    API endpoint to Get all Instagram processed data
    Can take query parameters, like date sorting , most recent, and by query string
    """
    return get_routes.get_instagram_analysis()


@api.route("/instagram/<string:insta_post_id>")
@token_auth.login_required
def get_single_instagram_analysis(insta_post_id):
    """_summary_

    Args:
        insta_post_id (_str_): _description_

    Returns:
        _type_: _description_
    """
    return get_routes.get_single_instagram_analysis(insta_post_id)


@api.route("/twitter/")
@token_auth.login_required
def get_all_twitter_analysis():
    """
    API endpoint to Get all Amazon processed data
    Can take query parameters, like date sorting , most recent, and by query string
    """
    return get_routes.get_all_twitter_analysis()


@api.route("/twitter/<string:search_query>")
@token_auth.login_required
def get_single_twitter_analysis(search_query):
    """
    API endpoint to Get all Amazon processed data
    Can take query parameters, like date sorting , most recent, and by query string
    """
    return get_routes.get_single_twitter_analysis(search_query)


@api.route("/facebook/")
@token_auth.login_required
def get_all_facebook_analysis():
    """
    API Endpoint to Get all the Facebook analysis by a user
    Can take query parameters, like date sorting , most recent, and by query string

    """
    return get_routes.get_all_facebook_analysis()


@api.route("/facebook/analysis/<string:post_id>")
@token_auth.login_required
def get_single_facebook_analysis(post_id):
    """
    API Endpoint to Get a single Facebook analysis by a user
    Can take query parameters, like date sorting , most recent, and by query string

    """
    return get_routes.get_single_facebook_page_post(post_id)


@api.route("/instagram/posts/<string:fb_page_id>")
@token_auth.login_required
def get_instagram_posts(fb_page_id):
    """
    API Endpoint to Get a single Facebook analysis by a user
    Can take query parameters, like date sorting , most recent, and by query string

    """
    return get_routes.get_ig_media_id(fb_page_id)


# ---------ECOMMMERCE VIEWS-----------


@api.route("/amazon/")
@token_auth.login_required
def get_amazon_analysis():
    """
    API endpoint to Get all Amazon processed data
    Can take query parameters, like date sorting , most recent, and by query string
    """

    return get_routes.get_amazon_analysis()


@api.route("/amazon/<string:product_name>/<string:product_id>")
@token_auth.login_required
def get_single_amazon_analysis(product_name, product_id):
    """_summary_

    Args:
        product_id (_type_): _description_
        product_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return get_routes.get_single_amazon(product_name, product_id)


@api.route("/konga/")
@token_auth.login_required
def get_konga_analysis():
    """_summary_

    Returns:
        _type_: _description_
    """
    return get_routes.get_all_konga()


@api.route("/konga/<string:product_description>")
@token_auth.login_required
def get_single_konga_analysis(product_description):
    """_summary_

    Args:
        product_description (_type_): _description_

    Returns:
        _type_: _description_
    """
    return get_routes.get_single_konga(product_description)


@api.route("/jumia/")
@token_auth.login_required
def get_all_jumia_analysis():
    """_summary_

    Returns:
        _type_: _description_
    """
    return get_routes.get_all_jumia()


@api.route("/jumia/<string:product_id>")
@token_auth.login_required
def get_single_jumia_analysis(product_id):
    """_summary_

    Args:
        product_id (_type_): _description_
    """

    return get_routes.get_single_jumia(product_id)
