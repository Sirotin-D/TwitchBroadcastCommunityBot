import config
all_commands_message = "Список команд бота:\n " \
                  "1) Стрим - узнать, идёт ли сейчас стрим\n" \
                  "2) График - узнать график стримов\n" \
                  "3) Команды - список всех команд"
greeting_message = "Здарова! {}".format(all_commands_message)
stream_schedule = "График стримов:\n " \
                  "Каждый день в 22:00\n" \
                  "Суббота - выходной"
stream_status = "Статус стрима: \n"
streamerNowOffline = "Стрим сейчас оффлайн"
streamerNowOnline = "Стрим сейчас онлайн!\n" \
                    "Скорее залетай на трансляцию\n {}" \
                    .format(config.twitch_channel_url)
