from typing import List

from nonebot import on_shell_command
from nonebot.params import ShellCommandArgv
from nonebot.exception import ParserExit
from nonebot.adapters.onebot.v11 import Event, MessageSegment

from .data import load_init_config
from .mcsm import MCSM
from .parser import mcsm_parser

try:
    from nonebot_plugin_htmlrender import text_to_pic
except ImportError:
    from nonebot.plugin import require

    text_to_pic = require("nonebot_plugin_htmlrender").text_to_pic

mcsm_ctl = on_shell_command("mcsm", parser=mcsm_parser, priority=10)


@mcsm_ctl.handle()
async def _(event: Event, argv: List[str] = ShellCommandArgv()):
    try:
        args = mcsm_parser.parse_args(argv)
        res = await handle_command(args, int(event.get_user_id()))

        await mcsm_ctl.finish(MessageSegment.image(await text_to_pic(str(res))))  # type: ignore
    except ParserExit as e:
        if e.status == 0:
            await mcsm_ctl.finish(
                MessageSegment.image(await text_to_pic(str(e.message)))
            )


async def handle_command(args, user_id: int):
    mcsm = MCSM(**load_init_config(user_id))
    if args.list:
        """列出服务器"""
        overview = await mcsm.overview
        instances = []
        for uuid in overview["data"]["remote"]["uuid"]:
            instances.append(await mcsm.remote_services_list(uuid))

        return
    elif args.add:
        """添加服务器"""
        pass
    elif args.user and args.server:
        """给予指定用户服务器操作的权限"""
        pass
    elif args.server:
        """获取服务器的信息"""
        pass
    elif args.server and args.action:
        """对服务器进行操作"""
        pass
    elif args.server and args.command:
        """在服务器内执行命令"""
        pass
    elif args.action:
        """询问服务器操作"""
        pass
