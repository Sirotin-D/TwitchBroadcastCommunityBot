import sys
import time
from threading import Thread
from Error.exceptions import TwitchError, VkError, NoFoundBroadcastError
from Services.messages_service import MessageService
from Twitch.Twitch import Twitch
from Vk.Vk import Vk
from DataClasses.Broadcast import Broadcast
from Config import private_config
from Config import api_config
from DataClasses.log_type import LogType
from Services.log_service import LogService


def query_answer_mode(twitch: Twitch, vk: Vk):
    vk.query_answer_mode(twitch=twitch)


def broadcast_newsletter_mode(twitch: Twitch, vk: Vk):
    is_notified: bool = False

    while True:
        try:
            broadcast: Broadcast = twitch.get_last_broadcast()
            if broadcast.is_live and not is_notified:
                streamer_message: str = MessageService.get_message_when_broadcast_is_live(title=broadcast.title,
                                                                                          category=broadcast.category)
                vk.send_newsletter(streamer_message)
                is_notified = True

            elif not broadcast.is_live:
                is_notified = False

        except NoFoundBroadcastError as no_found_broadcast_error:
            LogService.log(f"Error config: {no_found_broadcast_error}", log_type=LogType.CRITICAL)
            sys.exit()
        except TwitchError as twitch_error:
            LogService.log(f"Newsletter mode: error broadcast receiving: {twitch_error}", log_type=LogType.ERROR)
        except VkError as vk_error:
            LogService.log(f"Newsletter mode: vk error: {vk_error}", log_type=LogType.ERROR)
        time.sleep(api_config.twitch_waiting_request_seconds)


def main():
    twitch = Twitch(twitch_channel=private_config.twitch_channel_name)
    vk = Vk(auth_token=private_config.vk_test_access_token,
            group_id=private_config.vk_test_group_id)

    Thread(target=broadcast_newsletter_mode, args=(twitch, vk,)).start()
    Thread(target=query_answer_mode, args=(twitch, vk,)).start()


if __name__ == "__main__":
    main()
