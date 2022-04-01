from httpx import Response, AsyncClient


class MCSMAPIError(Exception):
    ...


class HTTPStatusError(Exception):
    ...


async def async_get(
    url: str,
    params: dict,
    headers: dict = {"Content-Type": "application/json; charset=utf-8"},
    **kwargs,
) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url,
            headers=headers,
            params=params,
            **kwargs,
        )
        return res.json()


def check(res: Response) -> int:
    if res.status_code != 200:
        raise HTTPStatusError("Error: " + str(res.status_code))

    if res.json()["status"] != 200:
        raise MCSMAPIError(res.json()["error"])

    return int(res.json()["status"])


class MCSM:
    def __init__(self, server: str, apikey: str):
        self.server = server
        """服务器地址"""
        self.apikey = apikey
        """用户生成的APIKEY"""
        # self.uuid = uuid
        # """守护进程的UUID"""

    @property
    async def overview(self) -> dict:
        """数据监控"""
        return await async_get(
            self.server + "/api/overview",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            params={"apikey": self.apikey},
        )

    @property
    async def remote_services_system(self) -> dict:
        """查看面板数据简报"""
        return await async_get(
            self.server + "/api/service/remote_services_system",
            params={"apikey": self.apikey},
        )

    async def instance(self, uuid, remote_uuid) -> dict:
        """获取远程实例详情信息"""
        return await async_get(
            self.server + "/api/instance",
            params={
                "apikey": self.apikey,
                "uuid": uuid,
                "remote_uuid": remote_uuid,
            },
        )

    async def remote_services_list(self, remote_uuid: str):
        """根据条件查询应用实例"""
        return await async_get(
            self.server + "/api/service/remote_service_instances",
            params={
                "apikey": self.apikey,
                "remote_uuid": remote_uuid,
                "page": 1,
                "page_size": 10,
            },
        )
