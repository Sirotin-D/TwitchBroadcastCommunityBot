import requests
import config


def post_request():
    url = config.auth_Twitch_URL
    data = {"client_id": config.client_id,
            "client_secret": config.secret_id,
            "grant_type": config.twitch_grant_type
            }
    response = requests.post(url=url, json=data)
    return response


def get_Twitch_access_token() -> str:
    response = post_request()
    jwt_access_token = response.json()
    try:
        access_token = jwt_access_token["access_token"]
    except Exception:
        access_token = ""

    return access_token


def get_request():
    url = config.twitch_search_channels_url + config.twitch_channel_name
    access_token = get_Twitch_access_token()
    headers = {
        "Client-ID": config.client_id,
        "Authorization": "Bearer %s" % access_token
    }

    response = requests.get(url=url, headers=headers)
    return response.json()
