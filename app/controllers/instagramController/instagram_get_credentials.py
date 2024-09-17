from config import Config


def getCredentials():
    cred = dict()
    cred["client_id"] = Config.FACEBOOK_APP_ID
    cred["client_secret"] = Config.FACEBOOK_APP_SECRET
    cred["graph_domain"] = "https://graph.facebook.com"
    cred["graph_version"] = "v14.0"
    cred["endpoint_base"] = cred["graph_domain"] + "/" + cred["graph_version"] + "/"

    return cred
