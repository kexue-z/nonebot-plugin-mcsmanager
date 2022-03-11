from typing import List
from multiprocessing.managers import Namespace

from nonebot import on_command, on_shell_command
from nonebot.rule import ArgumentParser
from nonebot.params import CommandArg, ShellCommandArgv
from nonebot.exception import ParserExit
from nonebot_plugin_htmlrender import text_to_pic
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment

parser = ArgumentParser("mcsm", description="MCSmanager 聊天控制台")
parser.add_argument(
    "-l",
    "--list",
    help="查看服务器列表和状态",
    action="store_true",
)
parser.add_argument(
    "-a",
    "--add",
    help="添加面板服务器: 服务器地址 APIKEY",
    action="store",
    nargs=2,
)
parser.add_argument(
    "-u",
    "--user",
    help="给予指定用户服务器操作的权限",
    action="store",
    nargs=1,
)
parser.add_argument(
    "-s",
    "--server",
    help="服务器名称, 当无操作时, 将会获取服务器的信息",
    action="store",
    nargs=1,
)
parser.add_argument(
    "action",
    help="对服务器进行操作 可选 start/on(开) stop/off(关) restart(重启) kill(强制结束)",
    choices=["start", "on", "stop", "off", "restart", "kill"],
    action="store",
    nargs="?",
)
parser.add_argument(
    "-c",
    "--command",
    help="在服务器内执行命令",
    action="store",
    nargs="*",
)

mcsm_ctl = on_shell_command("mcsm", parser=parser, block=True, priority=10)


@mcsm_ctl.handle()
async def _(argv: List[str] = ShellCommandArgv()):
    try:
        args = parser.parse_args(argv)
        res = await handle_command(args)

        await mcsm_ctl.finish(MessageSegment.image(await text_to_pic(str(res))))  # type: ignore
    except ParserExit as e:
        if e.status == 0:
            await mcsm_ctl.finish(MessageSegment.image(await text_to_pic(e.message)))


async def handle_command(args) -> str:
    if args.list:
        """列出服务器"""
        return args.list
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
