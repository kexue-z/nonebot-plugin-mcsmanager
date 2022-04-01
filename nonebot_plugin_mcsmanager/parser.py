from nonebot.rule import ArgumentParser

mcsm_parser = ArgumentParser("mcsm", description="MCSmanager 聊天控制台")
mcsm_parser.add_argument(
    "-l",
    "--list",
    help="查看服务器列表和状态",
    action="store_true",
)
mcsm_parser.add_argument(
    "-a",
    "--add",
    help="添加面板服务器: 服务器地址 APIKEY",
    action="store",
    nargs=2,
)
mcsm_parser.add_argument(
    "-u",
    "--user",
    help="给予指定用户服务器操作的权限",
    action="store",
    nargs=1,
)
mcsm_parser.add_argument(
    "-s",
    "--server",
    help="服务器名称, 当无操作时, 将会获取服务器的信息",
    action="store",
    nargs=1,
)
mcsm_parser.add_argument(
    "action",
    help="对服务器进行操作 可选 start/on(开) stop/off(关) restart(重启) kill(强制结束)",
    choices=["start", "on", "stop", "off", "restart", "kill"],
    action="store",
    nargs="?",
)
mcsm_parser.add_argument(
    "-c",
    "--command",
    help="在服务器内执行命令",
    action="store",
    nargs="*",
)
