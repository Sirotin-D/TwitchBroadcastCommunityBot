import time
from threading import Thread
from Twitch.Twitch import Twitch
from Vk.Vk import Vk
from Twitch.Broadcast import Broadcast
import config
import messages


def query_answer_mode(twitch: Twitch, vk: Vk):
    vk.query_answer_mode(twitch_channel=twitch)


def broadcast_newsletter_mode(twitch: Twitch, vk: Vk):
    is_notified: bool = False

    while True:
        broadcast: Broadcast = twitch.get_last_broadcast()

        if broadcast.is_live and not is_notified:
            is_notified = True
            members_id_list: list = vk.get_group_members_id_list()
            streamer_message: str = messages.get_newsletter_message_when_broadcast_live(title=broadcast.title,
                                                                                        category=broadcast.category)
            vk.send_newsletter(members_id_list, streamer_message)

        elif not broadcast.is_live:
            is_notified = False

        time.sleep(config.twitch_waiting_request_seconds)


def main():
    twitch = Twitch(twitch_channel=config.twitch_channel_name)
    vk = Vk(auth_token=config.vk_test_access_token,
            group_id=config.vk_test_group_id)

    thread_1 = Thread(target=broadcast_newsletter_mode,
                      args=(twitch, vk,))
    thread_2 = Thread(target=query_answer_mode,
                      args=(twitch, vk,))

    thread_1.start()
    thread_2.start()


if __name__ == "__main__":
    main()
