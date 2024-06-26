from pydantic import BaseModel


class Instance(BaseModel):
    id: int
    instance_uuid: str
    remote_uuid: str
    name: str
    url: str
    apikey: str
