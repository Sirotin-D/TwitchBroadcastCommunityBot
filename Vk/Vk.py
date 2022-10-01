import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import messages
from Twitch.Twitch import Twitch
from Twitch.Broadcast import Broadcast
from Services.request_service import RequestService
import config


class Vk:
    def __init__(self,
                 auth_token,
                 group_id):
        self.__auth_token = auth_token
        self.__vk_session = vk_api.VkApi(token=auth_token)
        self.__group_id = group_id

    def __vk_post_request(self, url: str, method: str, body: dict) -> dict:
        correct_url: str = "{vk_api_url}/{vk_api_method}".format(vk_api_url=url,
                                                                 vk_api_method=method)
        response: dict = RequestService.post_request(url=correct_url, body=body)
        return response

    def get_group_members_id_list(self) -> list:
        url: str = config.vk_api_request_url
        method: str = config.vk_get_group_members_method
        body: dict = {
            "v": config.vk_api_version,
            "access_token": self.__auth_token,
            "group_id": self.__group_id
        }
        vk_response: dict = self.__vk_post_request(url=url, method=method, body=body)
        members_id_list: list = vk_response["response"]["items"]
        return members_id_list

    def __send_message(self, user_id: str, message: str):
        try:
            self.__vk_session.method(config.vk_messages_send_method,
                                     {
                                         "user_id": user_id,
                                         "message": message,
                                         "random_id": 0
                                     })
        except Exception:
            pass

    def send_newsletter(self, user_id_list: list, message: str):
        for user_id in user_id_list:
            self.__send_message(user_id=user_id, message=message)

    def query_answer_mode(self, twitch_channel: Twitch):
        long_poll = VkLongPoll(self.__vk_session)
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if event.text.lower() == "привет":
                        stream_message = messages.greeting_message
                    elif event.text.lower() == "стрим":
                        broadcast: Broadcast = twitch_channel.get_last_broadcast()
                        stream_message = messages.get_broadcast_status_message(broadcast=broadcast)
                    elif event.text.lower() == "график":
                        stream_message = messages.stream_schedule
                    else:
                        stream_message = messages.all_commands_message

                    self.__send_message(user_id=event.user_id, message=stream_message)
