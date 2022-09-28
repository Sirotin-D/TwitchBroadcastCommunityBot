import config
import messages
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import twitch_requests


def writeMessage(user_id, message, vk_session):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": 0})


def checkLiveStream() -> str:
    broadcast_live = twitch_requests.is_broadcast_live()
    streamer_message = messages.stream_status
    if broadcast_live.is_broadcast_live():
        streamer_message = "{}\n" \
                           "Текущий стрим: {}\n" \
                           "Категория: {}\n" \
            .format(messages.streamerNowOnline,
                    broadcast_live.get_current_title_broadcast(),
                    broadcast_live.get_current_category_broadcast())
    else:
        streamer_message += messages.streamerNowOffline

    return streamer_message


def main():
    vk_session = vk_api.VkApi(token=config.auth_VK_token)
    longPoll = VkLongPoll(vk_session)

    for event in longPoll.listen():
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

                writeMessage(user_id=event.user_id, message=stream_message, vk_session=vk_session)


if __name__ == "__main__":
    main()
