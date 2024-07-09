from typing import List

from nonebot.adapters import Event

# from nonebot.params import EventMessage
from nonebot_plugin_alconna.uniseg import UniversalMessage

from .api_models.instances import Model as InstanceList
from .api_models.overview import Model as Overview
from .database_models import Users
from .mcsm_api import get_all_remote_instances, get_overview_data
from .models import Instance, Server


async def is_user_exists(event: Event = UniversalMessage()) -> bool:
    return await Users.exists(user_id=event.get_user_id())


async def get_servers_list(user_id: str) -> List[Server]:
    _server_info = await Users.filter(user_id=user_id).values_list(
        "nonebot_plugin_mcsmanager_server_info__url",
        "nonebot_plugin_mcsmanager_server_info__apikey",
    )
    servers: List[Server] = []

    for i in _server_info:
        sev = Server(url=i[0], apikey=i[1])
        servers.append(sev)

    return servers


async def get_all_instances(user_id: str) -> List[Instance]:
    ser_list = await get_servers_list(user_id)

    all_instances: List[Instance] = []
    id = 0

    # 遍历一个用户的所有服务器
    for s in ser_list:
        overview: Overview = await get_overview_data(url=s.url, apikey=s.apikey)

        # 遍历一个mcsm实例的所有远程
        for r in overview.data.remote:
            remote_name = r.system.hostname
            remote_uuid = r.uuid

            # 遍历一个远程中的所有实例
            instance_list: InstanceList = await get_all_remote_instances(
                url=s.url,
                apikey=s.apikey,
                remote_uuid=remote_uuid,
            )
            for i in instance_list.data.data:
                name = i.config.nickname
                instance_uuid = i.instanceUuid

                all_instances.append(
                    Instance(
                        id=id,
                        instance_uuid=instance_uuid,
                        remote_name=remote_name,
                        remote_uuid=remote_uuid,
                        name=name,
                        url=s.url,
                        apikey=s.apikey,
                    )
                )
                id += 1

    return all_instances
