import time
from vk_api.vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DataClasses.log_type import LogType
from Error.exceptions import VkError, TwitchError
from Services.log_service import LogService
from Services.messages_service import MessageService
from Twitch.Twitch import Twitch
from DataClasses.Broadcast import Broadcast
from Services.request_service import RequestService
from Config import private_config
from Config import api_config
from requests.exceptions import RequestException


class Vk:
    def __init__(self,
                 auth_token,
                 group_id):
        self.__auth_token = auth_token
        self.__vk_session = VkApi(token=auth_token)
        self.__group_id = group_id

    @staticmethod
    def create_keyboard() -> VkKeyboard:
        keyboard = VkKeyboard()
        keyboard.add_button("Стрим", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("График", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_openlink_button("Перейти на канал", link=private_config.twitch_channel_url)
        return keyboard

    def __get_group_members_id_list(self) -> list:
        body: dict = {
            "v": api_config.vk_api_version,
            "access_token": self.__auth_token,
            "group_id": self.__group_id
        }
        url: str = f"{api_config.vk_api_request_url}/{api_config.vk_get_group_members_method}"

        try:
            vk_response: dict = RequestService.post_request(url=url, body=body)
            members_id_list: list = vk_response["response"]["items"]
        except (RequestException, KeyError) as error:
            raise VkError(f"Error getting current group members id list from response: {error}")
        except Exception as undefined_error:
            raise VkError(f"Undefined error: {undefined_error}")

        return members_id_list

    def __send_message(self, user_id: str, message: str):
        keyboard = self.create_keyboard()
        try:
            self.__vk_session.method(api_config.vk_messages_send_method,
                                     {
                                         "user_id": user_id,
                                         "message": message,
                                         "random_id": 0,
                                         "keyboard": keyboard.get_keyboard()
                                     })
        except Exception:
            pass

    def send_newsletter(self, message: str):
        try:
            user_id_list: list = self.__get_group_members_id_list()
        except Exception as error:
            raise VkError(f"Error getting group members is list: {error}")

        for user_id in user_id_list:
            self.__send_message(user_id=user_id, message=message)

    def query_answer_mode(self, twitch: Twitch):
        long_poll = VkLongPoll(self.__vk_session)
        while True:
            try:
                for event in long_poll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        if event.text.lower() == "привет" \
                                or event.text.lower() == "start" \
                                or event.text.lower() == "старт":
                            answer_message = MessageService.get_greeting_message()
                        elif event.text.lower() == "стрим":
                            broadcast: Broadcast = twitch.get_last_broadcast()
                            answer_message = MessageService.get_broadcast_status_message(broadcast=broadcast)
                        elif event.text.lower() == "график":
                            answer_message = MessageService.get_schedule_stream_message()
                        else:
                            answer_message = MessageService.get_all_bot_commands_message()

                        self.__send_message(user_id=event.user_id, message=answer_message)
            except TwitchError as twitch_error:
                LogService.log(f"VK Q/A mode: error broadcast receiving: {twitch_error}", log_type=LogType.ERROR)
            except Exception as error:
                LogService.log(f"VK Q/A mode: undefined error: {str(error)}", log_type=LogType.ERROR)
                LogService.log(f"Waiting {api_config.twitch_waiting_request_seconds} seconds",
                               log_type=LogType.INFO)
                time.sleep(api_config.twitch_waiting_request_seconds)
