import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Twitch.Twitch import Twitch
from Twitch.Broadcast import Broadcast
from Services.request_service import RequestService
import config
import messages


class Vk:
    def __init__(self,
                 auth_token,
                 group_id):
        self.__auth_token = auth_token
        self.__vk_session = vk_api.VkApi(token=auth_token)
        self.__group_id = group_id

    def __get_group_members_id_list(self) -> list:
        body: dict = {
            "v": config.vk_api_version,
            "access_token": self.__auth_token,
            "group_id": self.__group_id
        }
        url: str = "{vk_api_url}/{vk_api_method}".format(vk_api_url=config.vk_api_request_url,
                                                         vk_api_method=config.vk_get_group_members_method)
        members_id_list = list()
        try:
            vk_response: dict = RequestService.post_request(url=url, body=body)
            members_id_list: list = vk_response["response"]["items"]
        except Exception as error:
            print(f"Error: {error}")
            raise Exception(f"Error getting group members id list: {error}")
        finally:
            return members_id_list

    def __send_message(self, user_id: str, message: str):
        keyboard = self.__create_keyboard()
        try:
            self.__vk_session.method(config.vk_messages_send_method,
                                     {
                                         "user_id": user_id,
                                         "message": message,
                                         "random_id": 0,
                                         "keyboard": keyboard.get_keyboard()
                                     })
        except Exception:
            pass

    def send_newsletter(self, message: str):
        user_id_list = list()
        try:
            user_id_list: list = self.__get_group_members_id_list()
        except Exception as error:
            print(f"Error getting group members: {error}")
            pass
        finally:
            for user_id in user_id_list:
                self.__send_message(user_id=user_id, message=message)

    def query_answer_mode(self, twitch: Twitch):
        long_poll = VkLongPoll(self.__vk_session)
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if event.text.lower() == "привет" or event.text.lower() == "start" or event.text.lower() == "старт":
                        answer_message = messages.greeting_message
                    elif event.text.lower() == "стрим":
                        try:
                            broadcast: Broadcast = twitch.get_last_broadcast()
                        except Exception as error:
                            print(f"Error getting last broadcast: {error}")
                            return
                        answer_message = messages.get_broadcast_status_message(broadcast=broadcast)
                    elif event.text.lower() == "график":
                        answer_message = messages.stream_schedule
                    else:
                        answer_message = messages.all_commands_message

                    self.__send_message(user_id=event.user_id, message=answer_message)

    def __create_keyboard(self) -> VkKeyboard:
        keyboard = VkKeyboard()
        keyboard.add_button("Стрим", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("График", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_openlink_button("Перейти на канал", link=config.twitch_channel_url)
        return keyboard
