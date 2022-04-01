from ._yaml import get_yaml_file, write_yaml_file


def add_server(server: str, apikey: str, user_id: int) -> None:
    """添加服务器"""
    data = get_yaml_file()
    data[user_id].append({"server": server, "apikey": apikey})
    write_yaml_file(data)


def load_init_config(user_id: int) -> list:
    """
    :说明: `load_init_config`
    > 加载初始化参数

    :参数:
      * `user_id: int`: qq号

    :返回:
      - `dict[str, str]`: {"server": "...", "apikey": "..."} 服务器地址 APIKEY
    """
    data = get_yaml_file()
    uid = str(user_id)
    return data[uid]
