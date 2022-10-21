from Repository import messages
from DataClasses.Broadcast import Broadcast


class MessageService:
    @staticmethod
    def get_greeting_message() -> str:
        return f"{messages.greeting_message} " \
               f"{MessageService.get_all_bot_commands_message()}"

    @staticmethod
    def get_all_bot_commands_message() -> str:
        return messages.all_commands_message

    @staticmethod
    def get_schedule_stream_message() -> str:
        return messages.stream_schedule

    @staticmethod
    def get_message_when_broadcast_is_live(title: str, category: str) -> str:
        return f"{messages.stream_now_online_message}\n" \
               f"{messages.current_title_stream_message} {title}\n" \
               f"{messages.current_category_stream_message} {category}\n"

    @staticmethod
    def get_broadcast_status_message(broadcast: Broadcast) -> str:
        streamer_message: str = messages.stream_status_message
        if broadcast.is_live:
            streamer_message = MessageService.get_message_when_broadcast_is_live(title=broadcast.title,
                                                                                 category=broadcast.category)
        else:
            streamer_message += messages.stream_now_offline_message

        return streamer_message
