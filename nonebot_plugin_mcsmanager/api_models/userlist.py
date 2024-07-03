from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Instance(BaseModel):
    instanceUuid: str
    daemonId: str


class Datum(BaseModel):
    uuid: str
    userName: str
    passWord: str
    passWordType: int
    salt: str
    permission: int
    registerTime: str
    loginTime: str
    instances: List[Instance]
    apiKey: str
    isInit: bool
    secret: str
    open2FA: bool


class Data(BaseModel):
    data: List[Datum]
    maxPage: int
    page: int
    pageSize: int
    total: int


class UserList(BaseModel):
    status: int
    data: Data
    time: int
