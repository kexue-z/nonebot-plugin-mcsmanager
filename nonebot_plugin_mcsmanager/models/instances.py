from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Config(BaseModel, extra="allow"):
    createDatetime: int
    crlf: int
    cwd: str
    enableRcon: bool
    endTime: Optional[int]
    lastDatetime: int
    nickname: str
    processType: str
    tag: List
    type: str
    updateCommand: str


class Datum(BaseModel, extra="allow"):
    config: Config
    instanceUuid: str
    started: int
    status: int


class Data(BaseModel, extra="allow"):
    data: List[Datum]
    maxPage: int
    page: int
    pageSize: int


class Model(BaseModel):
    data: Data
    status: int
    time: int
