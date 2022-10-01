
class Broadcast:
    def __init__(self, is_live, title, category):
        self.__is_live = is_live
        self.__title = title
        self.__category = category

    def is_broadcast_live(self):
        return self.__is_live

    def get_current_title_broadcast(self):
        return self.__title

    def get_current_category_broadcast(self):
        return self.__category
