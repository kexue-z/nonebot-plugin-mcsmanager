from .database_models import ServerInfo, PermittedInstantce, PermittedUser, AdminUser
from typing import Union, Optional, Literal, Tuple, List
from nonebot_plugin_alconna import At
from nonebot.log import logger
from .mcsm_api import call_instance as mcsm_call_instance
from .utils import get_permitteduser_instances_list

from .models import Instance


async def bind(url: str, apikey: str, user_id: str) -> Tuple[AdminUser, bool]:
    """
    :说明: `bind`
    > 绑定的mcms面板实例

    :参数:
      * `url: str`: url
      * `key: str`: key
      * `user: str`: user
    """

    serverinfo, _ = await ServerInfo.get_or_create(url=url, apikey=apikey)

    return await AdminUser.update_or_create(user_id=user_id, server=serverinfo)


async def add_user(
    admin_id: str,
    remote: str,
    instance: str,
    name: str,
    user_to_add: Union[str, At],
) -> Tuple[Optional[PermittedUser], bool]:
    user_id = user_to_add.target if isinstance(user_to_add, At) else user_to_add

    server_id_dict = await AdminUser.get_or_none(user_id=admin_id).values("server_id")

    if server_id_dict:
        server_id = server_id_dict.get("server_id")
        # server_info = await ServerInfo.get(id=server_id)

        p_ins, _ = await PermittedInstantce.get_or_create(
            instance_uuid=instance,
            remote_uuid=remote,
            name=name,
            server_info_id=server_id,
        )

        p_user, state = await PermittedUser.get_or_create(user_id=user_id)
        await p_user.permitted_instantce.add(p_ins)

        return p_user, state

    else:
        return None, False


async def get_instantce_list(user_id: str) -> Tuple[Optional[List[Instance]], bool]:
    if await PermittedUser.exists(user_id=user_id):
        return await get_permitteduser_instances_list(user_id=user_id), True
    else:
        return None, False


async def call_instance(
    action: Literal["open", "stop", "restart"],
    user_id: str,
    instance_name: str,
) -> Tuple[str, bool]:
    instances = await get_permitteduser_instances_list(user_id=user_id)

    _matched: Optional[Instance] = None

    for i in instances:
        if i.name == instance_name:
            _matched = i
            break

    if not _matched:
        return "404", False

    logger.debug(
        f"calliing {_matched.url} instantce {action} "
        f"{_matched.name}, remote_uuid {_matched.remote_uuid}, instance_uuid {_matched.instance_uuid}"
    )

    return await mcsm_call_instance(
        _matched.url,
        _matched.instance_uuid,
        _matched.remote_uuid,
        _matched.apikey,
        action,
    )
