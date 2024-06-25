from httpx import AsyncClient
from .models.instances import InstanceList
from enum import Enum


class StatusCode(Enum):
    busy = -1
    stopped = 0
    stopping = 1
    starting = 2
    running = 3


async def admin_get_all_instances(
    url: str, apikey: str, remote_uuid: str, status: StatusCode
) -> InstanceList:
    async with AsyncClient() as c:
        params = {
            "apikey": apikey,
            "daemonId": remote_uuid,
            "page": 1,
            "page_size": 100,
            "status": status.value,
        }
        res = c.get(f"{url}/api/service/remote_service_instances", params=params)
        return InstanceList(**res.json())
