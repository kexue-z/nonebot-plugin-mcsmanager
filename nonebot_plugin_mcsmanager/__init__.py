from typing import List

from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_tortoise_orm")

from arclet.alconna import Alconna, Args, Subcommand
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot_plugin_alconna import (
    CommandMeta,
    CommandResult,
    Match,
    UniMessage,
    on_alconna,
)

from .data_source import bind
from .mcsm_api import call_instance
from .models import Instance
from .utils import check_if_user, get_all_instances

USAGE = """私聊使用 mcsm bind 绑定面板服务器后
即可使用相关指令
"""


EXAMPLE = """mcsm bind url apikey userid
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
        "cmd",
        Args["server_name", str],
        Args["command", str],
        alias=["run", "执行"],
        help_text="运行实例指令",
    ),
    Subcommand(
        "bind",
        Args["url?", str],
        Args["key?", str],
        Args["user?", str],
        help_text="绑定服务器和APIkey，",
    ),
    meta=CommandMeta(
        description="MCSmanager 实例管理",
        usage=USAGE,
        example=EXAMPLE,
    ),
)


mcsm = on_alconna(command=alc, auto_send_output=True)


mcsm_status = mcsm.dispatch("status", rule=Rule(check_if_user))
mcsm_open = mcsm.dispatch("open", rule=Rule(check_if_user))
mcsm_stop = mcsm.dispatch("stop", rule=Rule(check_if_user))
mcsm_restart = mcsm.dispatch("restart", rule=Rule(check_if_user))
mcsm_cmd = mcsm.dispatch("cmd", rule=Rule(check_if_user))
mcsm_bind = mcsm.dispatch("bind")


@mcsm_bind.handle()
async def _(
    bot: Bot,
    evnet: Event,
):
    is_private = UniMessage.get_target(evnet, bot).private
    if not is_private:
        await mcsm_bind.finish(UniMessage.text("请在私聊中进行操作"))


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
    msg, _ = await bind(url, key, user)

    await matcher.finish(UniMessage.text(msg))


@mcsm_status.handle()
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
):
    # 如果是 mcsm on abc 则直接运行
    # 如果是 mcsm on 则打印一个服务器列表供选择，回复数字
    command_type = res.result.subcommands.keys().__iter__().__next__()
    user_id = event.get_user_id()

    state["command_type"] = command_type

    # 打印列表，供选择
    all_instances = await get_all_instances(user_id=user_id)
    if all_instances:
        msg = "请输入id来选择相应的实例\n"
        msg += "\n".join(
            [f"{i.id}. 远程: {i.remote_name} 实例: {i.name}" for i in all_instances]
        )
        await matcher.send(UniMessage.text(msg))
        state["all_instances"] = all_instances


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
    try:
        _id = int(id)
    except ValueError:
        await matcher.reject(UniMessage.text("输入的必须为数字, 请重新输入"))

    all_instances: List[Instance] = state["all_instances"]

    ins = all_instances[_id]

    res, status = await call_instance(
        url=ins.url,
        remote_uuid=ins.remote_uuid,
        instance_uuid=ins.instance_uuid,
        action=state["command_type"],
    )

    if status:
        await matcher.finish(UniMessage.text(f"指令发送成功，状态 {res}"))
    else:
        await matcher.finish(UniMessage.text(f"指令发送失败，状态 {res}"))
