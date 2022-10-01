import config
from Twitch.Broadcast import Broadcast
from dev_requests import RequestService


class Twitch:
    def __init__(self,
                 client_id: str,
                 secret_id: str,
                 twitch_channel: str):
        self.__access_token = ""
        self.__client_id = client_id
        self.__secret_id = secret_id
        self.__twitch_channel_name = twitch_channel

    def __auth(self):
        url: str = config.auth_twitch_url
        body: dict = {
            "client_id": self.__client_id,
            "client_secret": self.__secret_id,
            "grant_type": config.twitch_grant_type
        }
        response: dict = RequestService.post_request(url=url, body=body)
        try:
            self.__access_token: str = response["access_token"]
        except Exception:
            print("Error getting access token")

    def get_current_broadcast_status(self) -> Broadcast:
        self.__auth()

        url: str = config.twitch_search_channels_url + config.twitch_channel_name
        body: dict = {
            "Client-ID": config.client_id,
            "Authorization": "Bearer %s" % self.__access_token
        }
        response: dict = RequestService.get_request(url=url, body=body)

        channel_list = list()
        try:
            channel_list: list = response["data"]
        except Exception:
            print("Error getting channel_list")

        streamer = dict()
        for channel in channel_list:
            if channel["broadcaster_login"] == config.twitch_channel_name:
                streamer = channel
                break

        if len(streamer) != 0:
            current_broadcast = Broadcast(is_live=streamer["is_live"], title=streamer["title"],
                                          category=streamer["game_name"])
            return current_broadcast
        else:
            raise Exception("Not found broadcast channel")
