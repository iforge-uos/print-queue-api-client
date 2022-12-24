import print_queue_api_client.database_api


def database_api_factory(server_ip: str = "", server_port: str = "", api_key: str = ""):
    return print_queue_api_client.database_api.database_api(
        server_ip, server_port, api_key
    )
