from __future__ import annotations

from pydantic import BaseModel


class InstanceOutputlog(BaseModel):
    status: int
    data: str
    time: int
