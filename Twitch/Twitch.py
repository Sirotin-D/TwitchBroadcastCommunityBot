from datetime import datetime
from requests import RequestException
from Config import private_config
from Config import api_config
from DataClasses.log_type import LogType
from DataClasses.twitch_access_token import TwitchAccessToken
from DataClasses.Broadcast import Broadcast
from Error.exceptions import TwitchError, AuthError, NoFoundBroadcastError
from Services.log_service import LogService
from Services.request_service import RequestService


class Twitch:
    def __init__(self, twitch_channel: str):
        self.__access_token: TwitchAccessToken
        self.__twitch_channel_name = twitch_channel

    def __auth(self):
        if hasattr(self, "_Twitch__access_token") and datetime.now() < self.__access_token.expires_in:
            return

        LogService.log("Twitch authentication", log_type=LogType.INFO)
        url: str = api_config.twitch_api_auth_url
        body: dict = {
            "client_id": private_config.twitch_client_id,
            "client_secret": private_config.twitch_secret_id,
            "grant_type": api_config.twitch_grant_type
        }
        try:
            response: dict = RequestService.post_request(url=url, body=body)
            now_timestamp: float = datetime.timestamp(datetime.now())
            expires_in_timestamp: int = int(now_timestamp + response["expires_in"])
            expires_in_date: datetime = datetime.fromtimestamp(expires_in_timestamp)
            self.__access_token = TwitchAccessToken(token=response["access_token"],
                                                    expires_in=expires_in_date,
                                                    token_type=response["token_type"])
        except (RequestException, KeyError) as error:
            raise AuthError(f"Error getting access token from response: {error}")
        except Exception as undefined_error:
            raise AuthError(f"Undefined error: {undefined_error}")

    def get_last_broadcast(self) -> Broadcast:
        try:
            self.__auth()

            url: str = f"{api_config.twitch_api_search_channels_url}{self.__twitch_channel_name}"
            body: dict = {
                "Client-ID": private_config.twitch_client_id,
                "Authorization": f"Bearer {self.__access_token.token}"
            }

            response: dict = RequestService.get_request(url=url, body=body)
            channel_list: list = response["data"]
            for channel in channel_list:
                if channel["broadcaster_login"] == self.__twitch_channel_name:
                    current_broadcast = channel
                    return Broadcast(is_live=current_broadcast["is_live"],
                                     title=current_broadcast["title"],
                                     category=current_broadcast["game_name"])

            raise NoFoundBroadcastError("Not found broadcast channel")
        except (RequestException, KeyError) as error:
            raise TwitchError(f"Error getting broadcast from response: {error}")
        except AuthError as auth_error:
            raise TwitchError(f"Auth error: {auth_error}")
        except NoFoundBroadcastError as no_found_broadcast_error:
            raise NoFoundBroadcastError(no_found_broadcast_error)
        except Exception as undefined_error:
            raise TwitchError(f"Undefined error: {undefined_error}")
