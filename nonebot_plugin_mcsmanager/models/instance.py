from __future__ import annotations

from pydantic import BaseModel


class Data(BaseModel):
    instanceUuid: str


class Model(BaseModel):
    status: int
    data: Data
    time: int
