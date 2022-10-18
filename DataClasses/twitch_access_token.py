import datetime
from dataclasses import dataclass


@dataclass
class TwitchAccessToken:
    token: str
    expires_in: datetime
    token_type: str
