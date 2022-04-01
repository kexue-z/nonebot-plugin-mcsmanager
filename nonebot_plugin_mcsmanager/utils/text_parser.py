from pathlib import Path

import jinja2
from jinja2.environment import Template

try:
    from nonebot_plugin_htmlrender import md_to_pic
except ImportError:
    from nonebot.plugin import require

    md_to_pic = require("nonebot_plugin_htmlrender").md_to_pic

TEMPLATES_PATH = str(Path(__file__).parent / "templates")

env = jinja2.Environment(
    extensions=["jinja2.ext.loopcontrols"],
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    enable_async=True,
)


async def server_list_to_pic(server_list: list) -> bytes:
    all_server = []
    for server in server_list:
        all_server.append(server["data"]["data"])
    template = env.get_template("server_list.md.jinja")
    return await md_to_pic(await template.render_async(servers=all_server))
