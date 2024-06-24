from .database_models import ServerInfo, PermittedInstantce, PermittedUser, AdminUser
from typing import Union, Optional
from nonebot_plugin_alconna import At


async def bind(url: str, key: str, user: str) -> tuple[AdminUser, bool]:
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
    user_to_add: Union[str, At],
) -> tuple[Optional[PermittedUser], bool]:
    user_id = user_to_add.target if isinstance(user_to_add, At) else user_to_add

    if await AdminUser.get_or_none(user_id=user_id):
        p_ins, _ = await PermittedInstantce.get_or_create(
            instance_uuid=instance, remote_uuid=remote
        )
        p_user, state = await PermittedUser.get_or_create(user_id=user_id)
        await p_user.permitted_instantce.add(p_ins)

        return p_user, state

    else:
        return None, False


async def get_instantce_list(user_id: str):
    pass
