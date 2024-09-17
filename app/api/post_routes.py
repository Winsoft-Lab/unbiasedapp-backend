from . import api
from flask import jsonify, g, request
from flask_login import current_user
from app.api.errors import error_response, unauthenticated
from app.controllers.Ecommerce.amazon import begin_amazon_search
from app.controllers.Ecommerce.jumia import begin_jumia_search
from app.controllers.Ecommerce.konga import begin_konga_search
from app.controllers.twitterController.search_tweets import search_tweets
from ..controllers.instagramController.instagram_get_credentials import getCredentials
from ..controllers.instagramController.Insta_graph_api import InstagramGraphAPI
from app.controllers.facebookController.facebook_graph_api import (
    get_page_access_token,
    get_page_post_comments,
    get_page_post_comments_reply,
)
from app.models import (
    FacebookAnalysis,
    InstagramAnalysis,
    AmazonAnalysis,
    TwitterAnalysis,
    JumiaAnalysis,
    KongaAnalysis,
    User,
)
from app.api.authentication import basic_auth

from app import db
import pickle
import json


def search_tweet(q, count):
    """
    API Endpoint with query parameters query string(q) and count of words for searching tweets
        http://localhost:5000/api/v1/search-tweet/{search-query}/count={count}

    Response:
        Object: Dict_str
    """
    result = search_tweets(q, count)

    if result.num_tweets == 0:  # Check if the tweet object has tweets
        return error_response(
            500, "Unable to retrieve Tweets, check your internet and try again"
        )

    _tweet = pickle.dumps(result)

    analysis = TwitterAnalysis.query.filter_by(
        search_query=q, user_id=basic_auth.current_user().id
    ).first()

    if analysis is None:
        new_twitter_analysis = TwitterAnalysis(
            user_id=basic_auth.current_user().id, search_query=q, tweets=_tweet
        )
        db.session.add(new_twitter_analysis)
    else:
        request.method = "PUT"
        analysis.tweets = _tweet
    db.session.commit()
    return "", 201


def selenium_amazon(product_name, product_id):
    # result = dict()
    url = f"https://www.amazon.com/{product_name}/product-reviews/{product_id}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent"

    # cm_cr_dp_d_show_all_btm?

    search_result = begin_amazon_search(url)
    _search_result = json.dumps(search_result)

    product = AmazonAnalysis.query.filter_by(
        user_id=basic_auth.current_user().id, product_id=product_id
    ).first()

    if product is None:
        new_search = AmazonAnalysis(
            user_id=basic_auth.current_user().id,
            product_id=product_id,
            product_name=product_name,
            reviews=_search_result,
        )

        db.session.add(new_search)
    else:

        product.reviews = _search_result

    db.session.commit()

    # for i in range(0, len(search_result)):
    #     result[i] = search_result[i]

    return {"msg": "Data retrieved successfully"}, 201


def selenium_jumia(product_id):

    result = dict()
    url = f"https://www.jumia.com.ng/catalog/productratingsreviews/sku/{product_id}/"

    search_result = begin_jumia_search(url)
    _search_result = json.dumps(search_result)

    product = JumiaAnalysis.query.filter_by(
        product_id=product_id, user_id=basic_auth.current_user().id
    ).first()

    if product is None:
        new_search = JumiaAnalysis(
            user_id=basic_auth.current_user().id,
            product_id=product_id,
            reviews=_search_result,
        )

        db.session.add(new_search)
    else:

        product.reviews = _search_result
    db.session.commit()

    for i in range(0, len(search_result)):
        result[i] = search_result[i]

    return jsonify(result), 201


def selenium_konga(product_name_code_url):

    url = f"https://www.konga.com/product/{product_name_code_url}"

    search_result = begin_konga_search(url)
    _search_result = json.dumps(search_result)

    product_description = KongaAnalysis.query.filter_by(
        product_description=product_name_code_url, user_id=basic_auth.current_user().id
    ).first()

    if product_description is None:
        new_search = KongaAnalysis(
            user_id=basic_auth.current_user().id,
            product_description=product_name_code_url,
            reviews=_search_result,
        )
        db.session.add(new_search)
    else:
        product_description.reviews = _search_result
    db.session.commit()

    return {"msg": "Data retrieved successfully"}, 201


def instagram_comments(fb_page_id, insta_post_id):

    user = User.query.get(basic_auth.current_user().id)

    if user is None or user.fb_access_token is None:
        return unauthenticated("Please Login facebook to access api")

    params = getCredentials()

    params["access_token"] = user.fb_access_token

    params["ig_media_id"] = insta_post_id

    media_response = InstagramGraphAPI(**params).getComments()

    ig_comment_and_reply_list = []  # A list of IG Comments and replies as a single unit

    for i in media_response["data"]:
        # print(i)
        text_date = i["text"] + ">" + i["timestamp"]
        ig_comment_and_reply_list.append(text_date)
        if i.get("replies") != None:
            for j in i["replies"]["data"]:
                rep_date = j["text"] + ">" + j["timestamp"]
                ig_comment_and_reply_list.append(rep_date)

    analysis = InstagramAnalysis.query.filter_by(
        insta_post_id=insta_post_id, user_id=basic_auth.current_user().id
    ).first()
    _ig_comment_and_reply_list = json.dumps(ig_comment_and_reply_list)

    # SAVING TO DATABASE
    if analysis is None:
        new_analysis = InstagramAnalysis(
            user_id=basic_auth.current_user().id,
            fb_page=fb_page_id,
            insta_post_id=insta_post_id,
            comments=_ig_comment_and_reply_list,
        )

        db.session.add(new_analysis)
    else:
        analysis.comments = _ig_comment_and_reply_list

    db.session.commit()

    return {"msg": "Data successfully retrieved"}, 201


def instagram_hashtag(q):

    user = User.query.get(basic_auth.current_user().id)

    if user is None and user.fb_access_token is None:
        return unauthenticated("Please Login facebook to access api")

    params = getCredentials()

    params["access_token"] = user.fb_access_token
    params["page_id"] = user.fb_page_id

    ig_user_id_response = InstagramGraphAPI(**params).get_instagram_account_id()

    ig_user_id = ig_user_id_response["instagram_business_account"]["id"]
    params["instagram_account_id"] = ig_user_id
    params["hashtag_name"] = q

    hashtag_search_response = InstagramGraphAPI(**params).get_hashtagsInfo()

    key = "data"

    if key not in hashtag_search_response.keys():
        return {"msg": f"No data found for hashtag {q}"}

    hashtag_search_id = hashtag_search_response["data"][0]["id"]

    params["hashtag_id"] = hashtag_search_id

    _type = request.args.get("type")

    if _type not in ["top_media", "recent_media"]:

        _type = "recent_media"

    params["type"] = _type

    hashtag_media_response = InstagramGraphAPI(**params).get_hashtagMedia()

    return hashtag_media_response


def retrieve_posts_id(page_response):
    """A function that returns the post id from the page response"""

    post_id = page_response["posts"]["data"][1]["id"]

    return post_id


def facebook_page_post_comments(page_id, post_id):
    """A function that gets the comments from a particular facebook
    post using the page id and the page access token
    """

    user = User.query.get(basic_auth.current_user().id)

    if user is None or user.fb_access_token is None:
        return unauthenticated("Please login with Facebook to access facebook data")

    params = getCredentials()

    params["access_token"] = user.fb_access_token  # User access token

    params["page_id"] = page_id

    response = get_page_access_token(**params)

    page_access_token = response["access_token"]  # Page access token

    params["page_access_token"] = page_access_token

    params["page_post_id"] = post_id

    page_post_response = get_page_post_comments(**params)

    post_comments = page_post_response["data"]

    comment_reply_list = (
        []
    )  # Empty list of comment and replies as a single list content

    for i in range(len(post_comments)):
        comment = post_comments[i]["message"] + ">" + post_comments[i]["created_time"]

        comment_reply_list.append(comment)  # adding comment to list

        comment_id = post_comments[i]["id"]

        params["comment_id"] = comment_id

        page_post_comment_reply = get_page_post_comments_reply(**params)

        if (
            page_post_comment_reply["data"] != []
        ):  # checking if data exit i.e The comment has a reply
            for j in range(len(page_post_comment_reply["data"])):
                reply = (
                    page_post_comment_reply["data"][j]["message"]
                    + ">"
                    + page_post_comment_reply["data"][j]["created_time"]
                )

                comment_reply_list.append(reply)

    analysis = FacebookAnalysis.query.filter_by(
        fb_post_id=post_id, user_id=basic_auth.current_user().id
    ).first()
    _comment_reply_list = json.dumps(comment_reply_list)

    if analysis is None:
        new_analysis = FacebookAnalysis(
            user_id=basic_auth.current_user().id,
            fb_page=page_id,
            fb_post_id=post_id,
            comments=_comment_reply_list,
        )

        db.session.add(new_analysis)
    else:
        analysis.comments = _comment_reply_list

    db.session.commit()

    return {"msg": "Data successfully retrieved"}, 201
