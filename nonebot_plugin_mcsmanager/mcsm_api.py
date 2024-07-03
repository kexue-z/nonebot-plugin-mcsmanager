from typing import Literal

from httpx import AsyncClient

from .api_models.instance import Model as InstanceResp
from .api_models.instances import Model as InstanceList


async def admin_get_all_instances(
    url: str,
    apikey: str,
    remote_uuid: str,
) -> InstanceList:
    async with AsyncClient() as c:
        params = {
            "apikey": apikey,
            "daemonId": remote_uuid,
            "page": 1,
            "page_size": 100,
            "status": "",
            "instance_name": "",
        }
        res = await c.get(f"{url}/api/service/remote_service_instances", params=params)

        return InstanceList(**res.json())


async def call_instance(
    url: str,
    instance_uuid: str,
    remote_uuid: str,
    apikey: str,
    action: Literal["open", "stop", "restart"],
):
    async with AsyncClient() as c:
        params = {
            "uuid": instance_uuid,
            "daemonId": remote_uuid,
            "apikey": apikey,
        }
        res = await c.get(
            f"{url}/api/protected_instance/{action}",
            params=params,
        )

        try:
            i_resp = InstanceResp(**res.json())

            if i_resp.status == 200:
                return "ok", True
            else:
                return str(i_resp.data), False
        except:  # noqa
            pass

        return "error", False
