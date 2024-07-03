from __future__ import annotations

from pydantic import BaseModel


class Data(BaseModel):
    uuid: str


class User(BaseModel):
    status: int
    time: int
    data: Data
