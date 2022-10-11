import time
from datetime import datetime
from threading import Thread
from Twitch.Twitch import Twitch
from Vk.Vk import Vk
from DataClasses.Broadcast import Broadcast
from Config import private_config
from Config import api_config
import messages


def query_answer_mode(twitch: Twitch, vk: Vk):
    vk.query_answer_mode(twitch=twitch)


def broadcast_newsletter_mode(twitch: Twitch, vk: Vk):
    is_notified: bool = False

    while True:
        try:
            broadcast: Broadcast = twitch.get_last_broadcast()
            if broadcast.is_live and not is_notified:
                streamer_message: str = messages.get_newsletter_message_when_broadcast_live(title=broadcast.title,
                                                                                            category=broadcast.category)
                vk.send_newsletter(streamer_message)
                is_notified = True

            elif not broadcast.is_live:
                is_notified = False
        except Exception as error:
            error_message = "{date}. {message}".format(date=datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                                                       message=error)
            print(error_message)

        time.sleep(api_config.twitch_waiting_request_seconds)
        continue


def main():
    twitch = Twitch(twitch_channel=private_config.twitch_channel_name)
    vk = Vk(auth_token=private_config.vk_test_access_token,
            group_id=private_config.vk_test_group_id)

    thread_1 = Thread(target=broadcast_newsletter_mode,
                      args=(twitch, vk,))
    thread_2 = Thread(target=query_answer_mode,
                      args=(twitch, vk,))

    thread_1.start()
    thread_2.start()


if __name__ == "__main__":
    main()
