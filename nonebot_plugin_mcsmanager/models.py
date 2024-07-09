from pydantic import BaseModel


class Instance(BaseModel):
    id: int
    """从 0 开始"""
    instance_uuid: str
    remote_name: str
    remote_uuid: str
    name: str
    url: str
    apikey: str


class Server(BaseModel):
    url: str
    apikey: str
