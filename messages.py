from Config import private_config
from DataClasses.Broadcast import Broadcast

all_commands_message = "Список команд бота:\n " \
                       "1) Стрим - узнать, идёт ли сейчас стрим\n" \
                       "2) График - узнать график стримов\n" \
                       "3) Команды - список всех команд"
greeting_message = f"Здарова! {all_commands_message}"
stream_schedule = "График стримов:\n " \
                  "Каждый день в 19:00\n" \
                  "Суббота - выходной"
stream_status_message = "Статус стрима: \n"
stream_now_offline_message = "Стрим сейчас оффлайн"
stream_now_online_message = "Стрим сейчас онлайн!\n" \
                            "Скорее залетай на трансляцию\n " \
                            f"{private_config.twitch_channel_url}"


def get_newsletter_message_when_broadcast_live(title: str, category: str) -> str:
    return f"{stream_now_online_message}\n" \
           f"Текущий стрим: {title}\n" \
           f"Категория: {category}\n"


def get_broadcast_status_message(broadcast: Broadcast) -> str:
    streamer_message: str = stream_status_message
    if broadcast.is_live:
        streamer_message = get_newsletter_message_when_broadcast_live(title=broadcast.title,
                                                                      category=broadcast.category)
    else:
        streamer_message += stream_now_offline_message

    return streamer_message
