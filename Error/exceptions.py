class TwitchBroadcastCommunityException(Exception):
    pass


class TwitchError(TwitchBroadcastCommunityException):
    pass


class NoFoundBroadcastError(TwitchError):
    pass


class AuthError(TwitchError):
    pass


class VkError(TwitchBroadcastCommunityException):
    pass
