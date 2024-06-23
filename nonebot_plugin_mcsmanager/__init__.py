from typing import Union

from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_tortoise_orm")

from arclet.alconna import Alconna, Args, Option, Subcommand
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import (
    At,
    CommandMeta,
    Match,
    UniMessage,
    on_alconna,
)

USAGE = """使用 mcsm bind 绑定面板服务器后，即可使用相关的控制指令
使用mcsm add_user 可以将开关实例的权限授予相关用户。需要指定实例ID和远程ID
"""


EXAMPLE = """mcsm bind -u "http://127.0.0.1:23333" -k "abc123"
mcsm admin add_user -r "123abc" -i "123123
"""


alc = Alconna(
    "mcsm",
    Subcommand(
        "status",
        alias=["状态"],
        help_text="获取实例状态",
    ),
    Subcommand(
        "on",
        Args["server_name", str],
        alias=["开服", "启动"],
        help_text="启动实例",
    ),
    Subcommand(
        "off",
        Args["server_name", str],
        alias=["关服", "关闭"],
        help_text="关闭实例",
    ),
    Subcommand(
        "restart",
        Args["server_name", str],
        alias=["重启", "重开"],
        help_text="重启实例",
    ),
    Subcommand(
        "admin",
        Subcommand(
            "add_user",
            Args["remote?", str],
            Args["instance?", str],
            Args["user?", Union[At, str]],
            alias=["添加用户"],
            help_text="添加用户到可管理的实例的权限中",
        ),
        Subcommand(
            "delete_user",
            Args["user", Union[At, str]],
            alias=["del_user", "删除用户"],
            help_text="删除用户权限",
        ),
    ),
    Subcommand(
        "cmd",
        Option("-n|--server_name", Args["server_name", str]),
        Args["command", str],
        alias=["run", "执行"],
        help_text="运行实例指令",
    ),
    Subcommand(
        "bind",
        Args["url?", str],
        Args["key?", str],
        Args["user?", str],
        help_text="【仅限超级用户】绑定服务器和APIkey，",
    ),
    meta=CommandMeta(
        description="MCSmanager 实例管理",
        usage=USAGE,
        example=EXAMPLE,
    ),
)


mcsm = on_alconna(command=alc, auto_send_output=True)


mcsm_bind = mcsm.dispatch("bind", permission=SUPERUSER)
"""绑定操作"""


@mcsm_bind.handle()
async def _(
    bot: Bot,
    evnet: Event,
):
    is_private = UniMessage.get_target(evnet, bot).private
    if not is_private:
        await mcsm_bind.finish(UniMessage("请在私聊中进行操作"))


@mcsm_bind.handle()
async def bind_server_h(url: Match[str], key: Match[str], user: Match[str]):
    if url.available:
        mcsm_bind.set_path_arg("bind.url", url.result)

    if key.available:
        mcsm_bind.set_path_arg("bind.key", key.result)

    if user.available:
        mcsm_bind.set_path_arg("bind.user", user.result)

    logger.critical(f"{url} {key} {user}")


@mcsm_bind.got_path(
    "~url", prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请输入 url")
)
@mcsm_bind.got_path(
    "~key",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入 mcsm 的 apikey"
    ),
)
@mcsm_bind.got_path(
    "~user",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入接受绑定的用户 ID"
    ),
)
async def bind_server(
    url: str,
    key: str,
    user: str,
):
    pass


mcsm_admin_user_add = mcsm.dispatch("admin.add_user")


@mcsm_admin_user_add.handle()
async def admin_user_add_h(
    remote: Match[str],
    instance: Match[str],
    user: Match[Union[At, str]],
):
    if remote.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.remote", remote.result)
    if instance.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.instance", instance.result)
    if user.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.user", user.result)

    pass


@mcsm_admin_user_add.got_path(
    "~remote",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入 mcsm 的 remote_uuid"
    ),
)
@mcsm_admin_user_add.got_path(
    "~instance",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入 mcsm 的 instance_uuid"
    ),
)
@mcsm_admin_user_add.got_path(
    "~user",
    prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请输入用户或 At"),
)
async def admin_user_add(
    remote: str,
    instance: str,
    user: Union[str, At],
):
    pass


@mcsm.assign("status")
async def _(evnet: Event):
    pass


# TODO: ON OFF RESTART
