from Config import private_config
from DataClasses.Broadcast import Broadcast

all_commands_message = "Список команд бота:\n " \
                       "1) Стрим - узнать, идёт ли сейчас стрим\n" \
                       "2) График - узнать график стримов\n" \
                       "3) Команды - список всех команд"
greeting_message = "Здарова! {message_after_greeting}".format(message_after_greeting=all_commands_message)
stream_schedule = "График стримов:\n " \
                  "Каждый день в 19:00\n" \
                  "Суббота - выходной"
stream_status_message = "Статус стрима: \n"
stream_now_offline_message = "Стрим сейчас оффлайн"
stream_now_online_message = "Стрим сейчас онлайн!\n" \
                            "Скорее залетай на трансляцию\n {twitch_channel_url}" \
    .format(twitch_channel_url=private_config.twitch_channel_url)


def get_newsletter_message_when_broadcast_live(title: str, category: str) -> str:
    return "{broadcast_status}\n" \
           "Текущий стрим: {broadcast_title}\n" \
           "Категория: {broadcast_category}\n" \
        .format(broadcast_status=stream_now_online_message,
                broadcast_title=title,
                broadcast_category=category)


def get_broadcast_status_message(broadcast: Broadcast) -> str:
    streamer_message: str = stream_status_message
    if broadcast.is_live:
        streamer_message = get_newsletter_message_when_broadcast_live(title=broadcast.title,
                                                                      category=broadcast.category)
    else:
        streamer_message += stream_now_offline_message

    return streamer_message
