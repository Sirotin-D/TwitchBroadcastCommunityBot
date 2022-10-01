from dev_requests import RequestService
from Twitch.Broadcast import Broadcast
import config


def get_Twitch_access_token() -> str:
    url: str = config.auth_twitch_url
    body: dict = {
        "client_id": config.client_id,
        "client_secret": config.secret_id,
        "grant_type": config.twitch_grant_type
    }

    response: dict = RequestService.post_request(url=url, body=body)

    access_token: str
    try:
        access_token: str = response["access_token"]
    except Exception:
        access_token = ""

    return access_token


def get_current_broadcast_status() -> Broadcast:
    url: str = config.twitch_search_channels_url + config.twitch_channel_name
    access_token: str = get_Twitch_access_token()
    body: dict = {
        "Client-ID": config.client_id,
        "Authorization": "Bearer %s" % access_token
    }

    response: dict = RequestService.get_request(url=url, body=body)

    channel_list: list = response["data"]

    streamer = dict()
    for channel in channel_list:
        if channel["broadcaster_login"] == config.twitch_channel_name:
            streamer = channel
            break

    if len(streamer) != 0:
        current_channel = Broadcast(is_live=streamer["is_live"], title=streamer["title"],
                                    category=streamer["game_name"])
        return current_channel
    else:
        raise Exception("Not found broadcast channel")
