from ._yaml import get_yaml_file, write_yaml_file


def add_server(server: str, apikey: str, user_id: int) -> None:
    """添加服务器"""
    data = get_yaml_file()
    data[user_id].append({"server": server, "apikey": apikey})
    write_yaml_file(data)
