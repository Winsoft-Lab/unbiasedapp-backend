import requests
import json


def makeApiCall(url, endpointParams):
    """
    A function that sends a get request to the facebook graph API with the
    endpoint params.
    url= api url of the get request,
    endpointParams = API endpoint parameters for the target endpoint.
    """

    data = requests.get(url, endpointParams)

    response = json.loads(data.content)

    return response


def get_page_access_token(**params):

    """
    https://graph.facebook.com/{graph-version}/{PAGE-ID}?fields=access_token&access_token={user-access-token}

    Response: {
        "access_token":"PAGE-ACCESS-TOKEN",
        "id":"PAGE-ID"
        }

    """
    endpointParams = dict()
    endpointParams["fields"] = "access_token"
    endpointParams["access_token"] = params["access_token"]

    url = params["endpoint_base"] + params["page_id"]

    return makeApiCall(url, endpointParams)


def page_posts_id(**params):

    """
    Uses the page access token

    https://graph.facebook.com/{graph-version}/{page-id}?fields=posts


    returns a list of posts in the page

    """
    endpointParams = dict()
    endpointParams["access_token"] = params["page_access_token"]
    endpointParams["fields"] = "posts"
    url = params["endpoint_base"] + params["page_id"]

    return makeApiCall(url, endpointParams)


def get_page_post_comments(**params):

    """
    https://graph.facebook.com/{graph-version}/{page-post-id}/comments

    """
    endpointParams = dict()
    endpointParams["access_token"] = params["page_access_token"]
    url = params["endpoint_base"] + params["page_post_id"] + "/comments"

    return makeApiCall(url, endpointParams)


def get_page_post_comments_reply(**params):

    """
    https://graph.facebook.com/{graph-version}/{comment-id}/comments

    """
    endpointParams = dict()
    endpointParams["access_token"] = params["page_access_token"]
    url = params["endpoint_base"] + params["comment_id"] + "/comments"

    return makeApiCall(url, endpointParams)
