import dev_requests
from Broadcast import Broadcast
import config


def is_broadcast_live() -> Broadcast:
    response = dev_requests.GET_request()
    channel_list = response["data"]
    streamer = dict()
    for channel in channel_list:
        if channel["broadcaster_login"] == config.twitch_channel_name:
            streamer = channel
            break

    current_channel = Broadcast(is_live=streamer["is_live"], title=streamer["title"], category=streamer["game_name"])
    return current_channel
