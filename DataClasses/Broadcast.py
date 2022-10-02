from dataclasses import dataclass


@dataclass
class Broadcast:
    is_live: bool
    title: str
    category: str
