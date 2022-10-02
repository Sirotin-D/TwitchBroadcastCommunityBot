import config
from DataClasses.twitch_access_token import TwitchAccessToken
from Twitch.Broadcast import Broadcast
from Services.request_service import RequestService


class Twitch:
    def __init__(self, twitch_channel: str):
        self.__access_token: TwitchAccessToken
        self.__twitch_channel_name = twitch_channel

    def __auth(self):
        url: str = config.twitch_api_auth_url
        body: dict = {
            "client_id": config.twitch_client_id,
            "client_secret": config.twitch_secret_id,
            "grant_type": config.twitch_grant_type
        }
        try:
            response: dict = RequestService.post_request(url=url, body=body)
            self.__access_token = TwitchAccessToken(token=response["access_token"],
                                                    expires_in=response["expires_in"],
                                                    token_type=response["token_type"])
        except Exception as error:
            print(f"Error getting access token: {error}")
            return

    def get_last_broadcast(self) -> Broadcast:
        self.__auth()

        url: str = "{search_channels_url}{twitch_channel}".format(
            search_channels_url=config.twitch_api_search_channels_url,
            twitch_channel=self.__twitch_channel_name)
        body: dict = {
            "Client-ID": config.twitch_client_id,
            "Authorization": "Bearer %s" % self.__access_token.token
        }

        try:
            response: dict = RequestService.get_request(url=url, body=body)
            channel_list: list = response["data"]
            streamer = dict()
            for channel in channel_list:
                if channel["broadcaster_login"] == self.__twitch_channel_name:
                    streamer = channel
                    break
            if len(streamer) != 0:
                current_broadcast = Broadcast(is_live=streamer["is_live"],
                                              title=streamer["title"],
                                              category=streamer["game_name"])
            else:
                print("Not found broadcast channel")
                raise Exception("Not found broadcast channel")
        except Exception as error:
            print(f"Error: {error}")
            raise Exception(f"Error: {error}")

        finally:
            return current_broadcast
