import dev_requests
from Broadcast import Broadcast
import config


def get_Twitch_access_token() -> str:
    url = config.auth_twitch_url
    data = {"client_id": config.client_id,
            "client_secret": config.secret_id,
            "grant_type": config.twitch_grant_type
            }
    response = dev_requests.post_request(url=url, data=data)
    try:
        access_token = response["access_token"]
    except Exception:
        access_token = ""

    return access_token


def get_current_broadcast_status() -> Broadcast:
    url = config.twitch_search_channels_url + config.twitch_channel_name
    access_token = get_Twitch_access_token()
    headers = {
        "Client-ID": config.client_id,
        "Authorization": "Bearer %s" % access_token
    }
    response = dev_requests.get_request(url=url, data=headers)
    channel_list = response["data"]
    streamer = dict()
    for channel in channel_list:
        if channel["broadcaster_login"] == config.twitch_channel_name:
            streamer = channel
            break

    current_channel = Broadcast(is_live=streamer["is_live"], title=streamer["title"], category=streamer["game_name"])
    return current_channel
