from typing import Union

from arclet.alconna import Alconna, Args, Option, Subcommand
from nonebot_plugin_alconna import At, Match, on_alconna

alc = Alconna(
    "mcsm",
    Subcommand(
        "status",
        Option("-a|--all", help_text="所有实例"),
        alias=["状态"],
        help_text="获取实例状态，默认为已授权的实例，且已启动",
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
            Args["user", Union[At, str]],
            Option("-r|--remote_uuid", Args["remote", str], help_text="远程UUID"),
            Option("-i|--instance_uuid", Args["instance", str], help_text="实例UUID"),
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
)

# mcsm = on_alconna(command=alc)
