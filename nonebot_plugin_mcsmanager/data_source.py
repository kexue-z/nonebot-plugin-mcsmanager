from typing import Tuple

from .database_models import ServerInfo, Users


async def bind(url: str, apikey: str, user_id: str) -> Tuple[str, bool]:
    """
    :说明: `bind`
    > 绑定的mcms面板实例

    :参数:
      * `url: str`: url
      * `key: str`: key
      * `user_id: str`: user_id
    """

    user, _ = await Users.get_or_create(user_id=user_id)
    server, status = await ServerInfo.get_or_create(url=url, apikey=apikey, user=user)

    if status:
        return "已创建服务器信息", True
    else:
        return "服务器信息已存在", False
