import time
import config
import messages
from Twitch.Twitch import Twitch
from Vk.Vk import Vk
from Twitch.Broadcast import Broadcast
from threading import Thread


def query_answer_mode(twitch: Twitch, vk: Vk):
    vk.query_answer_mode(twitch_channel=twitch)


def broadcast_news_letter_mode(twitch: Twitch, vk: Vk):
    is_notified: bool = False
    while True:
        broadcast_live: Broadcast = twitch.get_current_broadcast_status()

        if broadcast_live.is_live and not is_notified:
            is_notified = True
            members_id_list: list = vk.get_group_members_id_list(group_id=config.vk_test_group_id)
            streamer_message: str = messages.get_newsletter_message_when_broadcast_live(title=broadcast_live.title,
                                                                                        category=broadcast_live.category)

            vk.make_news_letter(members_id_list, streamer_message)
        elif not broadcast_live.is_live:
            is_notified = False

        time.sleep(config.twitch_waiting_request_seconds)


def main():
    twitch = Twitch(client_id=config.client_id,
                    secret_id=config.secret_id,
                    twitch_channel=config.twitch_channel_name)
    vk = Vk(auth_token=config.auth_vk_token)

    thread_1 = Thread(target=broadcast_news_letter_mode,
                      args=(twitch, vk,))
    thread_2 = Thread(target=query_answer_mode,
                      args=(twitch, vk,))

    thread_1.start()
    thread_2.start()


if __name__ == "__main__":
    main()
