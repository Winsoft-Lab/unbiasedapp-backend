import time
from app.controllers.instagramController.Insta_graph_api import InstagramGraphAPI
from app.controllers.instagramController.instagram_get_credentials import getCredentials
from app.models import User
from . import auth
from app import oauth, db
import os
from flask import url_for, redirect, session, flash, request
from flask_login import login_user
import json


@auth.route("/facebook/")
def facebook_login():
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = os.environ.get("FACEBOOK_APP_ID")
    FACEBOOK_CLIENT_SECRET = os.environ.get("FACEBOOK_APP_SECRET")
    oauth.register(
        name="facebook",
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url="https://graph.facebook.com/oauth/access_token",
        access_token_params=None,
        authorize_url="https://www.facebook.com/dialog/oauth",
        authorize_params=None,
        api_base_url="https://graph.facebook.com/v14.0",
        client_kwargs={
            "scope": "email business_management instagram_basic public_profile pages_show_list pages_read_engagement pages_read_user_content"
        },  # email business_management instagram_basic page_read_engagement page_manage_posts page_manage_engagement
    )
    redirect_uri = url_for("auth.facebook_auth", _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@auth.route("/authorize/facebook/")
def facebook_auth():
    token = oauth.facebook.authorize_access_token()

    access_token = token["access_token"]

    params = getCredentials()
    params["access_token"] = access_token
    # session['fb_access_token'] = access_token

    response = InstagramGraphAPI(**params).debug_long_lived_token()

    page_response = InstagramGraphAPI(**params).get_account_info()

    if page_response["data"] == []:
        flash(
            "Please register your account as a business, create a page and link instagram to use unbiased analytics",
            category="info",
        )
        return redirect("/")

    page_list = []  # LIST OF ID and Name (key-value pair) OF THE PAGES THE USER MANAGES
    for i in range(len(page_response["data"])):
        id_name_dict = dict()
        id_name_dict[page_response["data"][i]["id"]] = page_response["data"][i]["name"]
        page_list.append(id_name_dict)

    resp = oauth.facebook.get("https://graph.facebook.com/v14.0/me?fields=email,name")
    profile = resp.json()
    email = profile["email"]
    username = profile["name"]
    fb_access_token = response["access_token"]
    password = profile["email"]

    user = User.query.filter_by(email=email).first()

    # LOGIN USER
    if user is not None:
        user.fb_page_id = json.dumps(
            page_list
        )  # Updates the users list of facebook pages
        db.session.commit()
        login_user(user)
        next = request.args.get("next")
        if next is None or not next.startswith("/"):
            next = url_for("main.home")
            return redirect(next)

    new_user = User(
        email=email,
        username=username,
        fb_access_token=fb_access_token,
        fb_page_id=json.dumps(page_list),
        password=password,
    )

    db.session.add(new_user)
    db.session.commit()
    flash("Registration successful")
    return redirect(url_for("auth.login"))


@auth.route("/twitter/")
def twitter_login():
    TWITTER_CLIENT_ID = os.environ.get("TWITTER_KEY")
    TWITTER_CLIENT_SECRET = os.environ.get("TWITTER_SECRET")
    oauth.register(
        name="twitter",
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url="https://api.twitter.com/oauth/request_token",
        request_token_params=None,
        access_token_url="https://api.twitter.com/oauth/access_token",
        access_token_params=None,
        authorize_url="https://api.twitter.com/oauth/authenticate",
        authorize_params=None,
        api_base_url="https://api.twitter.com/2/",
        client_kwargs=None,
    )
    redirect_uri = url_for("auth.twitter_auth", _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)


@auth.route("/authorize/twitter/")
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    # resp = oauth.twitter.get('account/verify_credentials.json')
    # profile = resp.json()
    # print(" Twitter User", profile)
    return redirect("/")
