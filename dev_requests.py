import requests
import config
import json
import string


def POST_request():
    url = config.authTwitchURL
    data = {"client_id": config.client_id,
            "client_secret": config.secret_id,
            "grant_type": config.twitch_grant_type
            }
    response = requests.post(url=url, json=data)
    return response


def get_access_token() -> string:
    response = POST_request()
    jwt_access_token = json.loads(response.content)
    try:
        access_token = jwt_access_token["access_token"]
    except:
        access_token = ""

    return access_token


def GET_request():
    url = config.twitch_search_channels_url + config.twitchChannel
    access_token = get_access_token()
    headers = {
        "Client-ID": config.client_id,
        "Authorization": "Bearer %s" % access_token
    }

    response = requests.get(url=url, headers=headers)
    return response.json()
