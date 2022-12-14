from Config import private_config

all_commands_message = "Список команд бота:\n" \
                       "1) Стрим - узнать, идёт ли сейчас стрим\n" \
                       "2) График - узнать график стримов\n" \
                       "3) Команды - список всех команд"

greeting_message = "Здарова!"

stream_schedule = "График стримов:\n" \
                  "Каждый день в 19:00\n" \
                  "Суббота - выходной"

stream_status_message = "Статус стрима:\n"

stream_now_offline_message = "Стрим сейчас оффлайн"

stream_now_online_message = "Стрим сейчас онлайн!\n" \
                            "Скорее залетай на трансляцию\n" \
                            f"{private_config.twitch_channel_url}"

current_title_stream_message = "Текущий стрим:"

current_category_stream_message = "Категория:"
