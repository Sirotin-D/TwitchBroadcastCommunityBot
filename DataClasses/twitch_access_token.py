from dataclasses import dataclass


@dataclass
class TwitchAccessToken:
    token: str
    expires_in: str
    token_type: str
