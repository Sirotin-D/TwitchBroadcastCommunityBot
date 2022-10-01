import time
import config
import messages
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Twitch.Broadcast import Broadcast
from Twitch import twitch_requests
from Vk import vk_requests
from threading import Thread

vk_session = vk_api.VkApi(token=config.auth_vk_token)


def get_newsletter_message_when_broadcast_live(title: str, category: str) -> str:
    return "{broadcast_status}\n" \
           "Текущий стрим: {broadcast_title}\n" \
           "Категория: {broadcast_category}\n" \
        .format(broadcast_status=messages.streamerNowOnline,
                broadcast_title=title,
                broadcast_category=category)


def get_broadcast_status_message() -> str:
    broadcast_live: Broadcast = twitch_requests.get_current_broadcast_status()
    streamer_message: str = messages.stream_status
    if broadcast_live.is_live:
        streamer_message = get_newsletter_message_when_broadcast_live(title=broadcast_live.title,
                                                                      category=broadcast_live.category)
    else:
        streamer_message += messages.streamerNowOffline

    return streamer_message


def vk_write_message(user_id: str, message: str):
    try:
        vk_session.method(config.vk_messages_send_method, {"user_id": user_id, "message": message, "random_id": 0})
    except Exception:
        pass


def vk_get_group_members_id_list() -> list:
    return vk_requests.vk_get_group_members_id_list(group_id=config.vk_test_group_id)


def vk_make_news_letter(user_id_list: list, message: str):
    for user_id in user_id_list:
        vk_write_message(user_id=user_id, message=message)


def query_answer_mode():
    long_poll = VkLongPoll(vk_session)
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.text.lower() == "привет":
                    stream_message = messages.greeting_message
                elif event.text.lower() == "стрим":
                    stream_message = get_broadcast_status_message()
                elif event.text.lower() == "график":
                    stream_message = messages.stream_schedule
                else:
                    stream_message = messages.all_commands_message

                vk_write_message(user_id=event.user_id, message=stream_message)


def broadcast_news_letter_mode():
    is_notified: bool = False
    while True:
        print(f"Current status notify: {is_notified}")
        broadcast_live: Broadcast = twitch_requests.get_current_broadcast_status()

        if broadcast_live.is_live and not is_notified:
            is_notified = True
            members_id_list: list = vk_get_group_members_id_list()
            streamer_message: str = get_newsletter_message_when_broadcast_live(title=broadcast_live.title,
                                                                               category=broadcast_live.category)

            vk_make_news_letter(members_id_list, streamer_message)
        elif not broadcast_live.is_live:
            is_notified = False

        time.sleep(config.twitch_waiting_request_seconds)


def main():
    thread_1 = Thread(target=broadcast_news_letter_mode, args=())
    thread_2 = Thread(target=query_answer_mode, args=())
    thread_1.start()
    thread_2.start()


if __name__ == "__main__":
    main()
