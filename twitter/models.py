from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """ """

    username: str = ""
    id: str = ""
    url: str = ""
    profileImageUrl: Optional[str] = None


@dataclass
class BaseTweet:
    """ """

    id: str = ""
    url: str = ""
    date: str = ""
    content: str = ""
    custom_user: Optional[User] = None


@dataclass
class Tweet(BaseTweet):
    """ """

    custom_replying_to: Optional[BaseTweet] = None
