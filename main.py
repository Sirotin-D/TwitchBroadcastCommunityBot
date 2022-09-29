import time
import config
import messages
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import twitch_requests
import vk_requests
from threading import Thread
vk_session = vk_api.VkApi(token=config.auth_vk_token)


def checkLiveStream() -> str:
    broadcast_live = twitch_requests.get_current_broadcast_status()
    streamer_message = messages.stream_status
    if broadcast_live.is_broadcast_live():
        streamer_message = "{broadcast_status}\n" \
                           "Текущий стрим: {broadcast_title}\n" \
                           "Категория: {broadcast_category}\n" \
            .format(broadcast_status=messages.streamerNowOnline,
                    broadcast_title=broadcast_live.get_current_title_broadcast(),
                    broadcast_category=broadcast_live.get_current_category_broadcast())
    else:
        streamer_message += messages.streamerNowOffline

    return streamer_message


def vk_write_message(user_id, message):
    try:
        vk_session.method(config.vk_messages_send_method, {"user_id": user_id, "message": message, "random_id": 0})
    except Exception:
        pass


def vk_get_group_members_id_list() -> list:
    return vk_requests.vk_get_group_members_id_list(group_id=config.vk_test_group_id)


def vk_make_news_letter(user_id_list, message):
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
                    stream_message = checkLiveStream()
                elif event.text.lower() == "график":
                    stream_message = messages.stream_schedule
                else:
                    stream_message = messages.all_commands_message

                vk_write_message(user_id=event.user_id, message=stream_message)


def broadcast_news_letter_mode():
    is_notified = False
    while True:
        broadcast_live = twitch_requests.get_current_broadcast_status()
        if broadcast_live.is_broadcast_live() and not is_notified:
            is_notified = True
            members_id_list = vk_get_group_members_id_list()
            streamer_message = "{broadcast_status}\n" \
                               "Текущий стрим: {broadcast_title}\n" \
                               "Категория: {broadcast_category}\n" \
                .format(broadcast_status=messages.streamerNowOnline,
                        broadcast_title=broadcast_live.get_current_title_broadcast(),
                        broadcast_category=broadcast_live.get_current_category_broadcast())

            vk_make_news_letter(members_id_list, streamer_message)
        elif not broadcast_live.is_broadcast_live():
            is_notified = False

        time.sleep(config.twitch_waiting_request_seconds)


def main():
    thread_1 = Thread(target=broadcast_news_letter_mode, args=())
    thread_2 = Thread(target=query_answer_mode, args=())
    thread_1.start()
    thread_2.start()


if __name__ == "__main__":
    main()
