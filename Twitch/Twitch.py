import config
from Twitch.Broadcast import Broadcast
from Services.request_service import RequestService


class Twitch:
    def __init__(self, twitch_channel: str):
        self.__access_token = ""
        self.__twitch_channel_name = twitch_channel

    def __auth(self):
        url: str = config.twitch_api_auth_url
        body: dict = {
            "client_id": config.twitch_client_id,
            "client_secret": config.twitch_secret_id,
            "grant_type": config.twitch_grant_type
        }
        response: dict = RequestService.post_request(url=url, body=body)
        try:
            self.__access_token: str = response["access_token"]
        except Exception:
            print("Error getting access token")

    def get_last_broadcast(self) -> Broadcast:
        self.__auth()

        url: str = config.twitch_api_search_channels_url + self.__twitch_channel_name
        body: dict = {
            "Client-ID": config.twitch_client_id,
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
            if channel["broadcaster_login"] == self.__twitch_channel_name:
                streamer = channel
                break

        if len(streamer) != 0:
            current_broadcast = Broadcast(is_live=streamer["is_live"], title=streamer["title"],
                                          category=streamer["game_name"])
            return current_broadcast
        else:
            raise Exception("Not found broadcast channel")
