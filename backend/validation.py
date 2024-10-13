from pydantic import BaseModel
# from typing import Optional


class FriendInfo(BaseModel):
    name: str
    role: str
    description: str
    gender: str