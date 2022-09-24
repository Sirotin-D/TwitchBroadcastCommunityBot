from typing import Any
import dev_requests
import config
import messages
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def is_broadcast_live() -> dict[str, Any]:
    response = dev_requests.GET_request()
    channel_list = response["data"]
    for channel in channel_list:
        if channel["broadcaster_login"] == config.twitchChannel:
            streamer = channel
            break

    return {"title_broadcast": streamer["title"], "game_name": streamer["game_name"], "is_live": streamer["is_live"]}


def writeMessage(user_id, message, vk_session):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": 0})


def checkLiveStream() -> str:
    broadcast_live = is_broadcast_live()
    streamer_message = messages.stream_status
    if broadcast_live["is_live"]:
        streamer_message += messages.streamerNowOnline
    else:
        streamer_message += messages.streamerNowOffline

    streamer_message += "\n Последний стрим: " + broadcast_live["title_broadcast"] + \
                        "\n Категория: " + broadcast_live["game_name"]

    return streamer_message


def main():
    vk_session = vk_api.VkApi(token=config.authVKToken)
    longPoll = VkLongPoll(vk_session)

    for event in longPoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.text.lower() == "привет":
                    writeMessage(event.user_id, messages.greeting_message, vk_session)
                elif event.text.lower() == "стрим":
                    stream_message = checkLiveStream()
                    writeMessage(event.user_id, stream_message, vk_session)
                elif event.text.lower() == "график":
                    writeMessage(event.user_id, messages.stream_schedule, vk_session)
                else:
                    writeMessage(event.user_id, messages.all_commands_message, vk_session)


if __name__ == "__main__":
    main()
