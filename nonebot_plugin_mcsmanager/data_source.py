from .database_models import ServerInfo, PermittedInstantce, PermittedUser, AdminUser
from typing import Union, Optional, Literal, Tuple
from nonebot_plugin_alconna import At
from httpx import AsyncClient, Response
from nonebot.log import logger
from .models.instance import Model as InstanceResp


async def bind(url: str, key: str, user: str) -> Tuple[AdminUser, bool]:
    """
    :说明: `bind`
    > 绑定的mcms面板实例

    :参数:
      * `url: str`: url
      * `key: str`: key
      * `user: str`: user
    """

    serverinfo, _ = await ServerInfo.get_or_create(url=url, key=key)

    return await AdminUser.update_or_create(user_id=user, server=serverinfo)


async def add_user(
    user_id: str,
    remote: str,
    instance: str,
    name: str,
    user_to_add: Union[str, At],
) -> Tuple[Optional[PermittedUser], bool]:
    user_id = user_to_add.target if isinstance(user_to_add, At) else user_to_add

    if await AdminUser.get_or_none(user_id=user_id):
        p_ins, _ = await PermittedInstantce.get_or_create(
            instance_uuid=instance,
            remote_uuid=remote,
            name=name,
        )
        p_user, state = await PermittedUser.get_or_create(user_id=user_id)
        await p_user.permitted_instantce.add(p_ins)

        return p_user, state

    else:
        return None, False


async def get_instantce_list(user_id: str):
    pass


async def call_instance(
    action: Literal["open", "stop", "restart"],
    user_id: str,
    instance_name: str,
) -> Tuple[str, bool]:
    _l = await PermittedUser.filter(user_id=user_id).values_list(
        "id",
        "permitted_instantce__instance_uuid",
        "permitted_instantce__remote_uuid",
        "permitted_instantce__name",
        "permitted_instantce__server_info__url",
        "permitted_instantce__server_info__apikey",
    )

    _matched: Tuple = ()
    for i in _l:
        if instance_name in i:
            _matched = i
            break

    if not _matched:
        return "404", False

    instance_uuid = _matched[1]
    remote_uuid = _matched[2]
    name = _matched[3]
    server_url = _matched[4]
    apikey = _matched[5]

    logger.debug(
        f"calliing {server_url} instantce {action} "
        f"{name}, remote_uuid {remote_uuid}, instance_uuid {instance_uuid}"
    )

    async with AsyncClient() as c:
        params = {
            "uuid": instance_uuid,
            "daemonId": remote_uuid,
            "apikey": apikey,
        }
        res = await c.get(
            f"{server_url}/api/protected_instance/{action}",
            params=params,
        )

        try:
            i_resp = InstanceResp(**res.json())

            if i_resp.status == 200:
                return "ok", True
        except:  # noqa
            return "error", False
