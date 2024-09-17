from app import oauth
import requests
import json


class InstagramGraphAPI:
    def __init__(self, *args, **params):
        self.params = params

    def makeApiCall(self, url, endpointParams):
        """
        A function that sends a get request to the facebook graph API with the
        endpoint params.
        url= api url of the get request,
        endpointParams = API endpoint parameters for the target endpoint.
        """

        data = requests.get(
            url, endpointParams
        )  # oauth.facebook.get(url, endpointParams)

        response = json.loads(data.content)  # data.json()

        return response

    def debug_long_lived_token(self):

        """
        API Endpoint:
        For generating long lived token
            https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
        """
        params = self.params

        url = params["endpoint_base"] + "oauth/access_token"

        # defining the endpoint parameters
        endpointParams = dict()

        endpointParams["grant_type"] = "fb_exchange_token"
        endpointParams["client_id"] = params["client_id"]
        endpointParams["client_secret"] = params["client_secret"]
        endpointParams["fb_exchange_token"] = params["access_token"]

        return self.makeApiCall(url, endpointParams)

    def get_account_info(self):

        """
        API Endpoint:
            Endpoint for ACCOUNTS info
            https://graph.facebook.com/{graph-version}/me/accounts?access_token={access_token}

        """
        params = self.params

        url = params["endpoint_base"] + "me/accounts"

        endpointParams = dict()
        endpointParams["access_token"] = params["access_token"]

        return self.makeApiCall(url, endpointParams)

    def get_instagram_account_id(self):

        """
        API ENDPOINT FOR GETTING INSTAGRAM INFO

            https://graph.facebook.com/{graph-version}/{page_id}?access_token={your-access-token}&f
            ields=instagram_business_account

        Returns:
        object: data from endpoint

        """

        params = self.params

        endpointParams = dict()
        endpointParams["fields"] = "instagram_business_account"
        endpointParams["access_token"] = params["access_token"]
        url = params["endpoint_base"] + params["page_id"]

        return self.makeApiCall(url, endpointParams)

    def get_user_media(self, pagingUrl=""):
        """
        Get User media

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_to
            ken={access-token}


        Returns:
            object: data from the endpoint

        """
        params = self.params

        endpointParams = dict()

        endpointParams[
            "fields"
        ] = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username"
        endpointParams["access_token"] = params["access_token"]

        json_data = []

        if "" == pagingUrl:
            url = params["endpoint_base"] + params["instagram_account_id"] + "/media"
            response = self.makeApiCall(url, endpointParams)
            json_data.append(response)
        else:
            url = pagingUrl
            response = self.makeApiCall(url, endpointParams)
            json_data.append(response)
            self.get_user_media(response["paging"]["next"])

        return json_data

    def getComments(self):

        """GET Comments from media
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-media-id}/comments?fields=like_count,replies,username,text'
        Returns
            object: data from the endpoint
        """
        params = self.params
        endpointParams = dict()
        endpointParams["fields"] = "like_count,replies,username,text,timestamp"
        endpointParams["access_token"] = params["access_token"]
        url = params["endpoint_base"] + params["ig_media_id"] + "/" + "comments"

        return self.makeApiCall(url, endpointParams)

    def get_hashtagsInfo(self):

        """
        API ENDPOINT:
            https://graph.facebook.com/{grap-api-version}/ig_hastag_search?user_id={
            user-id}&q={hastag-name}&fields={fields}&access_token={access_token}

        Returns:
            object: data from the endpoint

        """
        params = self.params

        endpointParams = dict()
        endpointParams["user_id"] = params["instagram_account_id"]
        endpointParams["q"] = params["hashtag_name"]
        endpointParams["fields"] = "id,name"
        endpointParams["access_token"] = params["access_token"]

        url = params["endpoint_base"] + "ig_hashtag_search"

        return self.makeApiCall(url, endpointParams)

    def get_hashtagMedia(self):
        """
        Get posts for a hashtag

        API Endpoints:
            https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top-media?u
            ser_id={user-id}&fields={fields}

            https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_medi
            a?user_id={user-id}&fields={fields}
        """
        params = self.params
        endpointParams = dict()
        endpointParams["user_id"] = params["instagram_account_id"]
        endpointParams[
            "fields"
        ] = "id,children,caption,comment_count,like_count,replies,media_type,media_url,permalink"
        endpointParams["access_token"] = params["access_token"]

        url = params["endpoint_base"] + params["hashtag_id"] + "/" + params["type"]
        return self.makeApiCall(url, endpointParams)
