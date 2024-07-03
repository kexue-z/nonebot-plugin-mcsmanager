from typing import Union, List

from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_tortoise_orm")

from arclet.alconna import Alconna, Args, Option, Subcommand
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot_plugin_alconna import (
    AlconnaMatch,
    At,
    CommandMeta,
    CommandResult,
    Match,
    UniMessage,
    on_alconna,
)


from .data_source import add_user, bind, call_instance, get_instantce_list
from .models import Instance
from .database_models import AdminUser

USAGE = """bot超管使用 mcsm bind 绑定面板服务器后
使用mcsm add_user 可以将开关实例的权限授予相关用户。需要指定实例ID和远程ID
"""


EXAMPLE = """【仅限bot超管】mcsm bind url apikey userid"
【仅限上方认证的管理】mcsm admin add_user name remote_uuid instance_uuid userid
"""


alc = Alconna(
    "mcsm",
    Subcommand(
        "status",
        alias=["状态"],
        help_text="获取实例状态",
    ),
    Subcommand(
        "open",
        Args["server_name?", str],
        alias=["start", "on", "开服", "启动"],
        help_text="启动实例",
    ),
    Subcommand(
        "stop",
        Args["server_name?", str],
        alias=["off", "关服", "关闭"],
        help_text="关闭实例",
    ),
    Subcommand(
        "restart",
        Args["server_name?", str],
        alias=["重启", "重开"],
        help_text="重启实例",
    ),
    Subcommand(
        "admin",
        Subcommand(
            "add_user",
            Args["name?", str],
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
mcsm_open = mcsm.dispatch("open")
mcsm_stop = mcsm.dispatch("stop")
mcsm_restart = mcsm.dispatch("restart")
mcsm_admin_user_add = mcsm.dispatch("admin.add_user")


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
    # TODO 不知道为什么 接受到AT之后就不会往下运行了
    "~user",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入接受绑定的用户 ID"
    ),
)
async def bind_server(
    matcher: Matcher,
    url: str,
    key: str,
    user: str,
):
    logger.debug(f"Adding bind server... {url} for {user}")
    _, res = await bind(url, key, user)
    if res:
        await matcher.finish(UniMessage.text("绑定成功"))
    else:
        await matcher.finish(
            UniMessage.text("绑定失败, 可能已经存在. 或已经被覆盖更新")
        )


@mcsm_admin_user_add.handle()
async def check_is_admin(event: Event, matcher: Matcher):
    if not await AdminUser.exists(user_id=event.get_user_id()):
        await matcher.finish("您不在管理员列表中")


@mcsm_admin_user_add.handle()
async def admin_user_add_h(
    name: Match[str],
    remote: Match[str],
    instance: Match[str],
    user: Match[Union[At, str]],
):
    if name.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.name", name.result)
    if remote.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.remote", remote.result)
    if instance.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.instance", instance.result)
    if user.available:
        mcsm_admin_user_add.set_path_arg("admin.add_user.user", user.result)


@mcsm_admin_user_add.got_path(
    "~name",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入服务器名称，用于快速操作"
    ),
)
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
    # TODO 不知道为什么 接受到AT之后就不会往下运行了
    "~user",
    prompt=UniMessage.template(
        "{:At(user, $event.get_user_id())} 请输入授权的用户或 At"
    ),
)
async def admin_user_add(
    matcher: Matcher,
    event: Event,
    remote: str,
    instance: str,
    name: str,
    user: Union[str, At],
):
    logger.debug(
        f"Adding user {user if isinstance(user, str) else user.target}\n"
        + "name: {name} remote: {remote} instance: {instance}"
    )

    p_user, status = await add_user(
        admin_id=event.get_user_id(),
        remote=remote,
        instance=instance,
        name=name,
        user_to_add=user,
    )

    if status and p_user:
        await matcher.finish(UniMessage.text(f"已添加 {p_user.user_id} 绑定 {name}"))

    else:
        await matcher.finish(UniMessage.text("绑定失败"))


@mcsm.assign("status")
async def _(event: Event):
    # TODO
    pass


@mcsm_open.handle()
@mcsm_stop.handle()
@mcsm_restart.handle()
async def call_ser_h(
    matcher: Matcher,
    event: Event,
    state: T_State,
    res: CommandResult,
    _server: Match[str] = AlconnaMatch("server_name"),
):
    # 如果是 mcsm on abc 则直接运行
    # 如果是 mcsm on 则打印一个服务器列表供选择，回复数字
    command_type = res.result.subcommands.keys().__iter__().__next__()
    user_id = event.get_user_id()

    state["command_type"] = command_type

    if _server.available:
        server_name = _server.result
        # TODO 有点冗余了 要改
        await call_instance(
            action=command_type,
            user_id=user_id,
            instance_name=server_name,
        )

        await matcher.finish(f"已经向 {server_name} 发送 {command_type} 指令")
    else:
        # 打印列表，供选择
        i_list, _ = await get_instantce_list(user_id)
        if i_list:
            msg = "请输入id来选择相应的实例\n"
            msg += "\n".join([f"{id+1}: {ins.name}" for id, ins in enumerate(i_list)])
            await matcher.send(msg)
            state["i_list"] = i_list

        else:
            await matcher.finish("你没有对此操作的权限")


@mcsm_open.got("id")
@mcsm_stop.got("id")
@mcsm_restart.got("id")
async def call_ser(
    matcher: Matcher,
    event: Event,
    state: T_State,
    id: str = ArgPlainText(),
):
    logger.debug(f"got id: {id}")
    _id = -1
    try:
        _id = int(id)
    except ValueError:
        await matcher.reject("输入的必须为数字, 请重新输入")

    i_list: List[Instance] = state["i_list"]

    ins = i_list[_id - 1]

    res, status = await call_instance(
        action=state["command_type"],
        user_id=event.get_user_id(),
        instance_name=ins.name,
    )

    if status:
        await matcher.finish(f"指令发送成功，状态 {res}")
    else:
        await matcher.finish(f"指令发送失败，状态 {res}")
